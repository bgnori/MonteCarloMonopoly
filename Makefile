
clean:
	rm *pyc; rm evoke.png

run:
	python main.py > log

test:
	python montecarlo.py > log

png:
	python graphcmd.py | dot -Tpng > evoke.png
