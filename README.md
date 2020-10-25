# Internet Archive Updater

Save your webisites in [archive.org](http://web.archive.org/) repeatedly using the free tier of [Heroku](https://heroku.com/).

![https://i.imgur.com/Bxmb9S1.png](https://i.imgur.com/Bxmb9S1.png)

## How to install it

**Clone** this repository:

```Bash
git clone https://github.com/MarcoDiFrancesco/InternetArchiveUpdater
```

**Change the URLs** you want Internet Archive to save in [links.txt](/links.txt). For example:

```txt
https://example.com/
https://www.facebook.com/
https://www.youtube.com/example
```

**Change how often to update** your web page in [clock.py](/clock.py). Default is 12 minutes:

```Python
@sched.scheduled_job("interval", minutes=12)
                                 ^^^^^^^^^^
OR
@sched.scheduled_job("interval", hours=3)
                                 ^^^^^^^
OR
@sched.scheduled_job("interval", days=1)
                                 ^^^^^^
```

**Set up an Heroku application**. If you are not familiar on how to run Python applications with Heroku follow this step-by-step YouTube tutorial by Andres Sevilla: [https://youtu.be/Ven-pqwk3ec](https://youtu.be/Ven-pqwk3ec?t=189) (start at 3:09)

Once the application is deployed in your `Heroku Dashboard` -> `Resources` you should see the `clock` task, you can enable it to run your application:

![https://i.imgur.com/AhI1wUO.png](https://i.imgur.com/AhI1wUO.png)

**Now your pages are being saved!**

# Internet Archive Website Uploader

Save your entire webisite in Internet Archive with only the domanin link given.

For example given the link in [scraper.py](/scraper.py):

```Plaintext
https://github.com/MarcoDiFrancesco
```

the program will follow all links inside the page to save pages like:

![https://i.imgur.com/s4aswN1.png](https://i.imgur.com/s4aswN1.png)

```Plaintext
https://github.com/MarcoDiFrancesco/DoexercisesTools
https://github.com/MarcoDiFrancesco/HomeAutomation
...
```

and will follow all links inside those pages:

```Plaintext
https://github.com/MarcoDiFrancesco/DoexercisesTools/blob/master/README.md
https://github.com/MarcoDiFrancesco/DoexercisesTools/blob/master/getMarks.py
...
```

and so on!

## Limitations

Currently in web.archive.org it's possible to upload 20093 pages per day. The program can anyway stay up for months without ever stopping.
