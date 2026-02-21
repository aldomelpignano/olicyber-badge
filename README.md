# Olicyber Badge Generator

A github workflow to generate cards like this:

![My Card](./card.svg)

# How To

## Auth Token
Go to the [Training Platform](training.olicyber.it), login. Then use the dev-tools to view the local storage and get your token.

![DevTools](https://raw.githubusercontent.com/utcq/oca/refs/heads/main/assets/devtools.png)
![Token](https://raw.githubusercontent.com/utcq/oca/refs/heads/main/assets/token.png)

---

## Methods

- [Automated Workflow](#automated-workflow)
- [Local Generation](#local-generation)

## Automated workflow
After forking the repo

> [!IMPORTANT]  
> go to **Settings -> Secrets and variables -> Actions**
>
> Create a new **Repository** secret named `OC_TOKEN` and insert the previously retrieved token

### Manual Update Trigger
The card is updated everyday at midnight (`UTC+1`) but you can update it manually:

Proceed to **Actions -> Generate Card (on the left) -> Run workflow**

When manually triggering the workflow, you can select a style from the dropdown menu:

![Screen](data/actions.png)

In the workflow run form, you'll see a "Card style" input field where you can choose between `default`, `dark`, `white`, or `darkRed`.

### Embedding
You now have to insert
```html
<img src="https://raw.githubusercontent.com/USER/ocbadge/main/card.svg"/>
```
in your github profile README
## Local Generation
```sh
export OC_TOKEN=*****
python3 gen.py style
```
Where style is optional and can be one of: `default`, `dark`, `white`, or `darkRed`.
The card will be saved in the execution dir as card.svg