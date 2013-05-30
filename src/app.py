from flask import Flask


class Constants:
    Version = '0.0.2'
    SupportedVersions = [ '0.0.1','0.0.2' ]

    @classmethod
    def toDict(cls):
        return {
            'Version':cls.Version,
            'SupportedVersions':cls.SupportedVersions
        }

####
####    The flask app ....
####

app = Flask(__name__)
app.debug = True
