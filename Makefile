
run:
	python montecarlo.py > log

png:
	python graphcmd.py | dot -Tpng > evoke.png
