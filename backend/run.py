from app import create_app
import os
from dotenv import load_dotenv
load_dotenv()
app = create_app()

print("PORT:", os.getenv('PORT'))

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(port=port, debug=True)