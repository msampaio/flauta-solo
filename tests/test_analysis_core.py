# -*- coding: utf-8 -*-

import unittest
import analysis.core as core
import analysis._utils as _utils

class TestUtils(unittest.TestCase):
    def test_makeCountry(self):
        name = 'Brazil'
        continent = 'America'

        country = core.Country()
        country.name = name
        country.continent = continent

        self.assertEqual(core.makeCountry(name, continent), country)
        self.assertNotEqual(core.makeCountry('Chile', continent), country)

    def test_makeCity(self):
        country = core.makeCountry('Brazil', 'America')
        name = 'Salvador'
        province = 'Bahia'

        fullCity = core.City()
        fullCity.name = name
        fullCity.country = country
        fullCity.province = province
        city = core.City()
        city.name = name
        city.country = country

        self.assertEqual(core.makeCity(name, country, province), fullCity)
        self.assertEqual(core.makeCity(name, country), city)
        self.assertNotEqual(core.makeCity('Juazeiro', country, province), fullCity)
        self.assertNotEqual(core.makeCity('Juazeiro', country), city)

    def test_makeComposer(self):
        country = core.makeCountry('Germany', 'Europe')
        completeName = 'Johann Sebastian Bach'
        gender = 'M'
        bornCityObj = core.makeCity('Eisenach', country)
        bornDate = '16850331'
        deathCityObj = core.makeCity('Leipzig', country)
        deathDate = '17500728'
        mainInstrument = 'Organ'

        composer = core.Composer()
        composer.prename, composer.name = _utils.nameParser(completeName)
        composer.gender = gender
        composer.bornCity = bornCityObj
        composer.bornDate = _utils.dateParser(bornDate)
        composer.deathCity = deathCityObj
        composer.deathDate = _utils.dateParser(deathDate)
        composer.mainInstrument = mainInstrument

        args1 = [completeName, gender, bornCityObj, bornDate, deathCityObj, deathDate, mainInstrument]
        args2 = [completeName, 'F', bornCityObj, bornDate, deathCityObj, deathDate, mainInstrument]

        self.assertEqual(core.makeComposer(*args1), composer)
        self.assertNotEqual(core.makeComposer(*args2), composer)

    def test_makeEditor(self):
        country = core.makeCountry('Belgium', 'Europe')
        completeName = 'Barthold Kuijken'
        gender = 'M'
        bornCityObj = core.makeCity('Dilbeek', country)
        bornDate = '19490308'
        deathCityObj = None
        deathDate = None

        editor = core.Editor()
        editor.prename, editor.name = _utils.nameParser(completeName)
        editor.gender = gender
        editor.bornCity = bornCityObj
        editor.bornDate = _utils.dateParser(bornDate)
        editor.deathCity = deathCityObj
        editor.deathDate = None
        args1 = [completeName, gender, bornCityObj, bornDate, deathCityObj, deathDate]
        args2 = [completeName, 'F', bornCityObj, bornDate, deathCityObj, deathDate]

        self.assertEqual(core.makeEditor(*args1), editor)
        self.assertNotEqual(core.makeEditor(*args2), editor)

    def test_makePiece(self):
        country = core.makeCountry('Germany', 'Europe')
        composer = core.makeComposer('Johann Sebastian Bach')

        title = 'Partita in A minor'
        subtitle = 'Flute solo'
        composerObj = composer
        cityObj = core.makeCity('Leipzig', country) # FIX
        date = '16850331' # FIX
        premierCityObj = core.makeCity('Leipzig', country) # FIX
        premierDate = '17500728' # FIX
        opus = None
        classificationCode = 'BWV 1013'
        movements = []
        structure = None
        tonality = 'A minor'

        piece = core.Piece()
        piece.title = title
        piece.subtitle = subtitle
        piece.composer = composerObj
        piece.city = cityObj
        piece.date = _utils.dateParser(date)
        piece.premierCity = premierCityObj
        piece.premierDate = _utils.dateParser(premierDate)
        piece.opus = opus
        piece.classificationCode = classificationCode
        piece.movements = movements
        piece.structure = structure
        piece.tonality = tonality

        args1 = [title, composerObj, tonality, date, subtitle, cityObj,
                 premierCityObj, premierDate, opus, classificationCode,
                 movements, structure]

        args2 = ['Partita in B minor', composerObj, tonality, date, subtitle, cityObj,
                 premierCityObj, premierDate, opus, classificationCode,
                 movements, structure]

        self.assertEqual(core.makePiece(*args1), piece)
        self.assertNotEqual(core.makePiece(*args2), piece)

    def test_makeMovement(self):
        title = 'Allemande'
        subtitle = None
        tempo = 'Allemande'
        tonality = 'A minor'

        movement = core.Movement()
        movement.title = title
        movement.subtitle = subtitle
        movement.tempo = tempo
        movement.tonality = tonality

        self.assertEqual(core.makeMovement(title, tempo, tonality, subtitle), movement)
        self.assertNotEqual(core.makeMovement('Presto', tempo, tonality, subtitle), movement)

    def test_makeSource(self):
        composer = core.makeComposer('Johann Sebastian Bach')
        editor = core.makeEditor('Michele Giulianini')
        piece = core.makePiece('Partita in A minor', composer)
        idCode = 'IF05673a'
        info = 'Michele Giulianini'

        source = core.Source()
        source.idCode = idCode
        source.piece = piece
        source.info = info
        source.editor = editor

        self.assertEqual(core.makeSource(idCode, piece, editor, info), source)
        self.assertNotEqual(core.makeSource('IF05673b', piece, editor, info), source)

if __name__ == '__main__':
    unittest.main()
