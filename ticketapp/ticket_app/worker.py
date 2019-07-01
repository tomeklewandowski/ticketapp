from faker import Factory
from random import choice
from .models import Event, Ticket, ticketsType, reservationStatus


def fake_event(locale="en_US"):
    fake = Factory.create(locale)
    t1 = ["Dni", "Wesele", "Tańce", "Dyskoteka", "Festiwal", "Gratka",
          "Gra", "Dane", "Zagadka", "Zabawa", "Programy"]

    t2 = ["Ucznia", "rycerza", "wojownika", "sportowców", "nauki","kierowców",
          "żołnierzy", "przyrody", "zwierząt", "w Polsce", "dla każdego"]

    e = Event()
    e.name = "{} {}".format(choice(t1), choice(t2))
    e.date = fake.date_this_year(before_today=True, after_today=False)
    print(e)
    e.save()


def populate_db():
    locales = ["pl-PL", "en-US", "es-ES", "de-DE", "cs-CZ", "fr-FR", "it-IT",
               "hr-HR", "nl-NL", "dk-DK", "fi-FI", "lt-LT", "pt-PT", "no-NO",
               "sv-SE", "tr-TR"]
    for i in range(0, 100):
        loc = choice(locales)
        fake_event(loc)
