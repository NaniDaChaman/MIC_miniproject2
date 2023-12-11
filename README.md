# mic-react-viz
This is Sparsh Amarnani's implementation of CS-6388-01 Model-Integrated Computing final mini project, a game studo for the othello game.
## Installation
To install this design studio. 


### Basic deployment
For a regular deployment, you need to install the following components on top of fetching this repository:
- [NodeJS](https://nodejs.org/en/) (LTS recommended)
- install Docker Desktop
- pull mongo db image from Docker Desktop
- Create a container for the image 
- when creating a container set Host port = 27017, container path =/data/db, give an appropriate host path
- Run the container 
- Fetch the repository

After all components in place, you need to install the dependencies, using `npm i` command and start your deployment 
using the `node ./app.js` command. If you have not changed the configuration, your design studio should be accessible on 
port 8888 of your localhost.

## Development
To make changes to this project you will need : 
going to need additional software:
- [NodeJS](https://nodejs.org/en/) (LTS recommended)
- [WebGME-CLI](https://www.npmjs.com/package/webgme-cli) (latest recommended)

You are going to use nodejs to bring in potentially new components or dependencies while the CLI is there to generate or import design studio components with handling the necessary config updates as well.

## Components
We are going to list the available components in this studio as well as describing how they can be created or what 
needs to be set for them to work as intended.

### Seed
There is a 2 seeds in the project representing the othello game - but all other default seeds are also available.

We use MetaModel_miniproject.webgmex.

### Meta
- prev : represents the previous gamestate, pointer from gamestate to gamestate
- currentstate : represents the current gamestate , pointer from gamefolder to gamestate
- Game : folder for various games being played
- currentPlayer : represents the previous games being played, from gamestate to piece 
- currentMove : represnts the previous piece being played, from gamestate to piece


### Plugin

- active_tiles: this plugin is written in python and returns the set of tiles from this project, ran from the game folder
- auto: this plugin is written in python and it plays an available move for the next player,ran from the game folder
- count_color: this plugin is written in python and returns the number of black and white coloured tiles,ran from the game folder
- undo : written in python, returns the game back to a previous game state,ran from the game folder
- flip_tiles : written in python, flips the pieces when invoked from a tile.
- since : our implementation of visualizer is incomplete please test this plugins with the run button by going to their respective nodes.
