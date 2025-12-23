# Twin Cities - South Metro Hockey Skating Events

## What this is?
This app aggregates Indoor Ice Arena events from numerous cites in the Twin Cities South Metro area. The general idea is to build a one-stop place to locate "Public Skate" and "Stick and Puck" events at these arenas. 

#### Public Skate:
- Public skate events are scheduled times at Ice Arenas where people can go Ice Skating
- Different arenas have different rules and prices; which I do my best to capture

#### Stick And Puck
- Stick and Puck or sometimes referred to as "Developmental Hockey" are the same as Public Skate, but people use Hockey Sticks and Hockey Pucks
- Worth noting that almost every arena does not allow people to setup games during these events. These are meant to be mostly solo events
- There are equipment requirements that differ per age group.
	- This app could be updated to start including those in the output

## Structure
- The app is made up of an API and a UI
- The API is python based and the UI is React based
- I use Docker Compose to build each as a stack
	- Each uses it's own Dockerfile for the build process
	- I use multi-stage builds for extra security
	- I do use a docker compose global env file to provide flexibility to set parameters per run env
- I do my best to lock down the containers as read-only except for what is needed
- There are also labels that are meant for [Traefik](https://doc.traefik.io/traefik/reference/install-configuration/providers/docker/); which is what I personally use as a proxy and cert management
	- My traefik setup puts the UI container behind a subdomain I have configured, but if you append "/api" you are sent to the API container
		- This is essential for client side communication; which is how the UI calls the API for data. Browser's will throw a fit if you try to cross over to another site that uses a different cert. By keeping them under the same subdomain(and same cert) client browsers have no issues pulling in the data

## Running
* To run the app simply clone the repo and run `./run.sh`; which will trigger the docker compose commands
	* **NOTE:** You are required to have a docker compose env file and that file **MUST** have a `DOCKER_CONFIG_PARENT_DIR` parameter with a value that points to where you cloned the app.

## Adding arenas, PRs, etc...
- I am very open to PRs, suggestions, etc...
