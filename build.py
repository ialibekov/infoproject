from app.search import Search
from mongoengine import connect

connect('infodb')

if __name__ == '__main__':
    search = Search()
    search.build()
