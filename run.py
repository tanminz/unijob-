
from App import create_app   # với điều kiện thư mục bạn đặt là "App" chứ không phải "app"


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


