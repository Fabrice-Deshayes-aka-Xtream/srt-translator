import re
import sys
import config

subtitle_separator = "<XTR/>"
packets_size = 1000


def progressbar(count_value, total, suffix=''):
    """
    Displays a text-based progress bar in the console.

    This function calculates the progress of a task and displays a progress bar
    in the console using '=' characters to indicate completion and '-' characters
    to indicate remaining progress.

    :param count_value: The current count of completed items.
    :type count_value: int
    :param total: The total count of items in the task.
    :type total: int
    :param suffix: A string to be appended to the progress bar (optional).
    :type suffix: str
    """
    bar_length = 100  # Total length of the progress bar
    filled_up_length = int(round(bar_length * count_value / float(total)))  # Calculate filled length
    percentage = round(100.0 * count_value / float(total), 1)  # Calculate completion percentage

    # Construct the progress bar with '=' and '-' characters
    bar = '=' * filled_up_length + '-' * (bar_length - filled_up_length)

    # Display the progress bar with percentage and suffix, overwrite the current line
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percentage, '%', suffix))
    sys.stdout.flush()  # Flush the output to update the progress bar immediately


def clean_sentence(sentence=""):
    """
    Cleans a given sentence by removing hearing impaired annotations and extra spaces.
    The function also checks the config.removeHearingImpairedAnnotations flag to determine whether to perform the cleaning or not.

    This function takes a sentence as input and performs cleaning operations,
    such as removing annotations enclosed in parentheses or brackets, and
    replacing multiple consecutive spaces with a single space.

    :param sentence: The sentence to be cleaned.
    :type sentence: str
    :return: The cleaned sentence.
    :rtype: str
    """

    if config.removeHearingImpairedAnnotations:
        # Remove annotations enclosed in parentheses, e.g., (...)
        sentence = re.sub(r'\([^)]*\)', "", sentence)
        # Remove annotations enclosed in brackets, e.g., [...]
        sentence = re.sub(r'|\[[^\]]*\]', "", sentence)
        # Remove annotation enclosed in asterix, e.g., *...*
        sentence = re.sub(r'\*.*?\*', "", sentence)

    if config.removeTags:
        # Remove HTML/XML tags, e.g., <...>
        sentence = re.sub(r'<[^>]*>', "", sentence)

    # Replace multiple consecutive spaces with a single space
    sentence = re.sub("\ {1,}", " ", sentence)

    # Remove subtitle_separator in subtitles as we used it as separator
    # sentence = sentence.replace(subtitle_separator, '')

    # replace line feed \n with subtitle_separator tag
    sentence = re.sub(r'\n', subtitle_separator, sentence)

    return sentence  # Return the cleaned sentence


def split_srt(srt_file):
    """
    Splits and processes SubRip (SRT) subtitle files.

    This function reads an SRT file, extracts technical information (sequence number and timecode),
    and organizes the subtitle text into cleaned sentences. Each subtitle consists of a sequence
    number, a timecode, and one or more lines of cleaned text.

    :param srt_file: The path to the input SRT file.
    :type srt_file: str
    :return: A tuple containing two lists - technical_info and subtitles.
             - technical_info: List of technical information, containing sequence numbers and timecodes.
             - subtitles: List of cleaned subtitle sentences, organized by sequence.
    :rtype: tuple[list[str], list[str]]
    """
    # Initialize two lists to store technical information and subtitles
    technical_info = []  # Stores sequence number and timecode
    subtitles = []  # Stores cleaned lines of subtitles
    current_index = 0  # Keeps track of the current line index in the file

    # Open the SRT file for reading with UTF-8 encoding and a BOM (Byte Order Mark)
    with open(srt_file, 'r', encoding='utf_8_sig') as f_srt:
        lines = f_srt.readlines()  # Read all lines from the file
        nb_lines = len(lines)  # Calculate the total number of lines in the file

        # Process each line in the SRT file
        while current_index < nb_lines:
            technical_info.append(lines[current_index])  # Store sequence number
            technical_info.append(lines[current_index + 1])  # Store timecode
            subtitles.append(clean_sentence(lines[current_index + 2]))  # Store cleaned first line of text
            current_index += 3  # Move the index forward by 3 to skip the processed lines

            # Process additional lines of text for the same subtitle
            while current_index < nb_lines and lines[current_index].strip() != '':
                subtitles.append(clean_sentence(lines[current_index]))  # Store cleaned other line of text
                current_index += 1  # Move the index forward

            current_index += 1  # Move the index forward to skip the empty line between subtitles
            subtitles.append(subtitle_separator)  # Append an empty string to indicate the end of this subtitle

    return technical_info, subtitles  # Return the collected technical info and cleaned subtitles


def merge_srt(srt_file, technical_info, subtitles):
    """
    Merges technical information and subtitles to create an SRT file.

    This function takes technical information (sequence numbers and timecodes)
    and subtitles as input and merges them to create an SRT file. Each subtitle
    consists of a sequence number, a timecode, and one or more lines of text.

    :param srt_file:
    :type srt_file: TextIO
    :param technical_info: List of technical information, containing sequence numbers and timecodes.
    :type technical_info: list[str]
    :param subtitles: List of subtitle sentences, organized by sequence.
    :type subtitles: list[str]
    """
    current_index_subtitles = 0  # Keeps track of the current subtitle index
    nb_lines_subtitles = len(subtitles)  # Total number of subtitle lines
    current_index_technical_info = 0  # Keeps track of the current technical info index
    nb_lines_technical_info = len(technical_info)  # Total number of technical info lines

    # Iterate through technical info and subtitles
    while current_index_technical_info < nb_lines_technical_info - 1 and current_index_subtitles < nb_lines_subtitles:
        # Write sequence number
        srt_file.write(technical_info[current_index_technical_info])
        # Write timecode
        srt_file.write(technical_info[current_index_technical_info + 1])
        # Write first line of text
        srt_file.write(subtitles[current_index_subtitles] + '\n')
        current_index_technical_info += 2
        current_index_subtitles += 1

        # Manage other lines of text for the same subtitle
        while current_index_subtitles < nb_lines_subtitles and subtitles[current_index_subtitles].strip() != '':
            srt_file.write(subtitles[current_index_subtitles] + '\n')
            current_index_subtitles += 1
        current_index_subtitles += 1
        srt_file.write('\n')  # Write a newline to separate subtitles


def fix_anomaly(subtitles):
    subtitles = [s.strip() for s in subtitles]  # remove trailing space on each subtitle line

    i = 0

    for line in subtitles:
        # fix line which start with a '.'' (we should be on previous line)
        if i > 0 and line.startswith('.') and subtitles[i - 1] != '':
            subtitles[i - 1] = subtitles[i - 1] + '.'
            subtitles[i] = line.lstrip('.')

        # fix line which start with a ':' (we should be on previous line)
        if i > 0 and line.startswith(':') and subtitles[i - 1] != '':
            subtitles[i - 1] = subtitles[i - 1] + ' :'
            subtitles[i] = line.lstrip(':')

        i += 1

    subtitles = [s.strip() for s in subtitles]  # remove trailing space on each subtitle line
    subtitles = [re.sub("\ {1,}", " ", s) for s in subtitles]  # replace many space by one space

    return subtitles
