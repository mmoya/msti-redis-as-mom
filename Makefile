redis-as-mom.pdf: redis-as-mom.tex memcache-example.tex
	pdflatex $^

memcache-example.tex: memcache-example.py
	pygmentize -O linenos=True -f latex $^ >$@

clean:
	rm -f *.aux
	rm -f *.blg
	rm -f *.dvi
	rm -f *.idx
	rm -f *.log
	rm -f *.nav
	rm -f *.out
	rm -f *.toc
	rm -f *.snm
	rm -f memcache-example.tex
	rm -f redis-as-mom.pdf

.PHONY: clean
