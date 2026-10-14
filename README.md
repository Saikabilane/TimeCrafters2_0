# TimeCrafters 2.0 — Constraint-Aware Timetable Generation

TimeCrafters 2.0 is a Python project exploring automated academic timetable generation. It represents faculty availability and scheduling constraints, reads timetable-related data from CSV files, and experiments with genetic-algorithm approaches to search for workable schedules.

## How it works
1. **Input data:** CSV files provide sample scheduling data used by the scripts.
2. **Constraint modelling:** `constraints.py` defines a teacher availability model; `constraintchecker.py` contains checks used to assess timetable validity.
3. **Schedule generation:** `timetable.py` and related scripts contain alternative scheduling approaches.
4. **Optimization experiments:** `GeneticAlgorithm.py` and `GeneticAlgorithm3.py` explore genetic-algorithm-based schedule search.
5. **Exploration:** `supreme.ipynb` provides a notebook-based workspace for experiments and inspection.

The repository contains multiple numbered and iterative Python scripts, so treat them as alternative experiments rather than assuming every file is part of one single production pipeline.

## Requirements
- Python 3.9+ recommended
- pandas (used for tabular data in the scheduling workflow)
- Jupyter Notebook, if you want to explore `supreme.ipynb`

Install the likely core dependencies:
```bash
git clone https://github.com/Saikabilane/TimeCrafters2_0.git
cd TimeCrafters2_0
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install pandas notebook
```

## Running
Start with the specific script you want to inspect, for example:
```bash
python timetable.py
```
The scripts may expect the CSV files to remain in the project directory. Check each script's input paths and configuration before running it; the repository currently contains several versions with different entry points.

## Scheduling considerations
A timetable generator should distinguish hard constraints (which must never be violated, such as teacher or room clashes) from soft preferences (which can be optimized). Review the generated timetable and constraint-checking output before relying on a schedule.

## Status
Research/prototype code. The repository does not currently define one documented command that runs every experiment end-to-end.

## License
No license file is currently included; contact the repository owner for reuse permission.
