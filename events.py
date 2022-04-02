import weather

import spacy
import datetime
import nltk

nlp = spacy.load('en_core_web_lg')
stemmer = nltk.stem.PorterStemmer()

events = list()


def get_time_from_text(text) -> (datetime.time, str):
    doc = nlp(text)

    for entity in doc.ents:
        if entity.label_ == "TIME":
            if ':' in entity.text:
                if 'PM' in entity.text:
                    time = datetime.time(hour=entity.text.split(':')[0] + 12,
                                         minute=entity.text.split(':')[1])
                    return time, entity.text
                else:
                    time = datetime.time(hour=entity.text.split(':')[0],
                                         minute=entity.text.split(':')[1])
                    return time, entity.text
            elif 'AM' in entity.text:
                time = datetime.time(hour=entity.text.split(':')[0])
                return time, entity.text
            elif 'PM' in entity.text:
                time = datetime.time(hour=entity.text.split(':')[0] + 12)
                return time, entity.text
    return None, ''


def add_event(text):
    place = weather.get_geopolitical_entity_from_text(text)
    delta_days, date_str = weather.get_delta_days_from_text(text)
    time, time_str = get_time_from_text(text)
    print(place, date_str, time_str)

    tokens = nltk.word_tokenize(text)  # Split the text into words
    tagged_words = nltk.pos_tag(tokens)  # Get a tag to each word in the text
    text = text

    if text.find("plan") != -1:
        word_start = text.find("plan")
        word_end = word_start + 4
        del tagged_words[text.split().index(text[word_start:word_end])]
        text = text[:word_start] + text[word_end + 1:]

    if text.find("event") != -1:
        word_start = text.find("event")
        word_end = word_start + 5
        prev_word_end = word_start - 1
        prev_word_start = prev_word_end
        while prev_word_start > 1 and text[prev_word_start - 1] != ' ':
            prev_word_start -= 1

        print(prev_word_start, prev_word_end, text[prev_word_start:prev_word_end])
        if prev_word_start != prev_word_end \
                and tagged_words[text.split().index(text[prev_word_start:prev_word_end])][1] == 'DT':
            del tagged_words[text.split().index(text[prev_word_start:prev_word_end])]
            text = text[:word_start] + text[prev_word_end + 1:]
        else:
            del tagged_words[text.split().index(text[word_start:word_end])]
            text = text[:word_start] + text[word_end + 1:]

    if place:
        word_start = text.find(place)
        word_end = word_start + len(place)
        prev_word_end = word_start - 1
        prev_word_start = prev_word_end
        while prev_word_start > 1 and text[prev_word_start - 1] != ' ':
            prev_word_start -= 1

        if prev_word_start != prev_word_end \
                and tagged_words[text.split().index(text[prev_word_start:prev_word_end])][1] == 'IN':
            del tagged_words[text.split().index(text[prev_word_start:prev_word_end])]
            text = text[:prev_word_start] + text[word_end + 1:]
        else:
            del tagged_words[text.split().index(text[word_start:word_end])]
            text = text[:word_start] + text[word_end + 1:]

    if date_str:
        word_start = text.find(date_str)
        word_end = word_start + len(date_str)
        prev_word_end = word_start - 1
        prev_word_start = prev_word_end - 1
        while prev_word_start > 1 and text[prev_word_start - 1] != ' ':
            prev_word_start -= 1
        print(word_start, word_end, text[word_start:word_end + 1], prev_word_start, prev_word_end, text[prev_word_start:prev_word_end])
        print(tagged_words[text.split().index(text[prev_word_start:prev_word_end])])
        print(text.split(), text.split().index(text[prev_word_start:prev_word_end]))

        if prev_word_start != prev_word_end \
                and tagged_words[text.split().index(text[prev_word_start:prev_word_end])][1] == 'IN':
            del tagged_words[text.split().index(text[prev_word_start:prev_word_end])]
            text = text[:prev_word_start] + text[word_end + 1:]
        else:
            del tagged_words[text.split().index(text[word_start:word_end])]
            text = text[:word_start] + text[word_end + 1:]

    if time_str:
        if text.find(time_str) != -1:
            word_start = text.find(time_str)
            word_end = word_start + len(time_str)
            prev_word_end = word_start - 1
            prev_word_start = prev_word_end - 1
            while prev_word_start > 1 and text[prev_word_start - 1] != ' ':
                prev_word_start -= 1

            if prev_word_start != prev_word_end \
                    and tagged_words[text.split().index(text[prev_word_start:prev_word_end])][1] == 'IN':
                del tagged_words[text.split().index(text[prev_word_start:prev_word_end])]
                text = text[:prev_word_start] + text[word_end + 1:]
            else:
                del tagged_words[text.split().index(text[word_start:word_end])]
                text = text[:word_start] + text[word_end + 1:]

    events.append({"name": text.strip(),
                   "date": datetime.date.today() + datetime.timedelta(days=delta_days),
                   "time": time, "place": place})
    print(events)
