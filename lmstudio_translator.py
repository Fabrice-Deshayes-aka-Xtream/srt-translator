import lmstudio as lms
import config


def translate_text(text_to_translate):
    model = lms.llm(config.model)
    result = model.respond(config.prompt + text_to_translate)
    return result.content
