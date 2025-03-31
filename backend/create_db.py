from app import app, db, User  # Passe 'app' an, falls dein Flask-App-Name anders ist

with app.app_context():
    # Überprüfe, ob der Benutzer bereits existiert
    existing_user = User.query.filter_by(username='admin').first()
    if not existing_user:
        # Erstelle den Benutzer
        admin_user = User(username='admin', password='password123')
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")