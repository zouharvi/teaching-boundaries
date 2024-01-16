# Teaching Boundaries of AI Performance

For scripts an analysis:

```bash
# add current directory to Python path
export PYTHONPATH=.:$PYTHONPATH

# generate a random decision tree for AI performance
python3 analysis/scripts/01-random_decision_tree.py
```

![random decision tree boundary](https://github.com/zouharvi/teaching-boundaries/assets/7661193/d3813cd7-e512-4cbc-874d-3544adb8cf17)

For user interface:

```bash
cd web
npm install
npm run dev # live version
npm run build # static artefact
```