import random
import string
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Generate the mnemonic
        mnemonic = '#' + ''.join(random.choices(string.ascii_letters + string.digits, k=7))

        # Process the sign-up form data
        username = request.form['username']
        # ... additional form fields and sign-up logic ...

        return render_template('success.html', mnemonic=mnemonic, username=username)
    else:
        return render_template('signup.html')

if __name__ == '__main__':
    app.run()