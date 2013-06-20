
clean:
	rm *pyc; rm evoke.png

run:
	python main.py > log

smoke:
	python -m pypoly.montecarlo > log

png:
	python graphcmd.py | dot -Tpng > evoke.png
