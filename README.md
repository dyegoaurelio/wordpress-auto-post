# WordPress Auto Post
This is a script a made a couple of years ago for learning purposes which scrapes news from News Sites and automatically publish on any WordPress Website

### Installation

clone this repository 

```bash
git clone https://github.com/dyegoaurelio/wordpress-auto-post.git
```

install requeriments

```bash
cd wordpress-auto-post && pip install -r requirents.txt
```

### Testing

If you want to check if the News Source you want will be correctly scraped you can run.
```bash
python3 urlscrape.py
```
and them provide a url from a news within the desired site.

### Running
insert your website information on ```auth.json```

then just run
```bash
python3 publicarWP.py
```
and then the script will ask for you to  provide each news url followed by it category, tag and date to publish.


