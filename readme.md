docker run -it --name website -v $PWD:/srv/jekyll -p 35729:35729/tcp -p 4000:4000/tcp arnoldschan/website:1.2.0
