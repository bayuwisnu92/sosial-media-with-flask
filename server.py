from app import create_app
app = create_app()
if __name__ == '__main__':
    # Menjalankan aplikasi dengan debug mode sesuai konfigurasi
    app.run(debug=True)