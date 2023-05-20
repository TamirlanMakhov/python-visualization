from encost_dash.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run_server(debug=True)

