# Simple External Cheat (Undetected by VAC)

### Features
- [x] Glow
- [x] Anti Flash
- [x] Rank Reveal
- [x] Radar Hack
- [ ] Add UI for Toggle

### How to use
1. Install Python 3 from https://www.python.org/downloads/ or the Windows Store. (When installing python, remember to tick "Add Python to PATH").
2. Install [https://code.visualstudio.com/](VSCode).
    - I am using Visual Studio Code as my IDE (You may select any IDE of your choice), remember to run it as Administrator.
3. In IDE Terminal, run ```pip install -r requirement.txt``` to install required libraries.
4. Join a game first.
5. Click on ```CSGOExternalCheat.py``` and on the top toolbar, click Run > Run Without Debugging

### FAQ
#### pip install did not work doesnt work
- Go search for file path ```%appdata%/Local/Programs/Python/Python3._``` ( _ depends on the python version number. Ex. 3.8 / 3.9 ) and right click copy this address as text, and the other file path ```%appdata%/Local/Programs/Python/Python3._/Scripts```
- Next, Search under your windows search for Edit System Environment Variables> Environment Variables
- Double click on the word PATH under User Variables, for each address, create new and paste it in.
- Do the same for Path under System Variables. Then Restart your computer.
