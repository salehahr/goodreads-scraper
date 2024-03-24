from grscraper import Config, Session, Shelf, sign_in

config = Config.from_file("config.yaml")

with Session() as session:
    sign_in(config, session)

    shelf = Shelf(config)
    shelf.populate(session)

    print(f"User #{config.user_id} has {len(shelf)} books on shelf '{config.shelf}'.")
