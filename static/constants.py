import re

from fuzzywuzzy import fuzz

standard_words = {
    'JavaScript': ['JS', 'Javascript', 'javascript'],
    'TypeScript': ['typescript', 'Typescript'],
    'Python': ['python'],
    'Java': ['java', 'Java8', 'java8', 'Java11', 'java11'],
    'Kotlin': ['kotlin'],
    'Ruby': ['ruby'],
    'Node.js': ['NodeJs', 'NodeJS', 'node.js', 'Node.js', 'Node', 'node'],
    'HTML': ['HTML5'],
    'JSON': ['Json', 'json'],
    'jQuery': ['Jquery', 'JQuery', 'jquery'],
    'MongoDB': ['mongo', 'Mongo', 'MongoDb', 'mongodb', 'Mongo DB'],
    'Test-Driven Development': ['Test Driven Development', 'TDD'],
    'EcmaScript': ['ES2015', 'ES5', 'ES6', 'ES5/ES6', 'ES', 'ES7', 'EcmaScript', 'Ecmascript', 'ES2018', 'ES2015/2016+',
                   'ES2015+'],
    'MySQL': ['MySql',],
    'C': ['c'],
    'C++': ['c++', ],
    'Elixir': ['elixir'],
    'CSS': ['css', 'CSS3', 'css3', 'CSS4', 'css4'],
    'Erlang': ['erlang'],
    'Go': ['GO', 'go', 'Golang', 'GoLang'],
    'React': ['react', 'react.js'],
    'Ruby on Rails': ['Rails', 'rails', 'ruby on rails'],
    'Django': ['django',]
}

if __name__ == '__main__':
    for standard_word, other_words in standard_words.items():
        for other_word in other_words:
            ratio = fuzz.partial_ratio(re.sub(r"[^a-zA-Z0-9]+", ' ', standard_word).lower(), re.sub(r"[^a-zA-Z0-9]+", ' ', other_word).lower())
            print(f'{standard_word} and {other_word} score is {ratio}')