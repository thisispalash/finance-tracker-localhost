# Localhost Expense Tracker
> Started as final project for Encode Club's AI Bootcamp

This project is to manage personal finances. Currently, it is really simple in that you upload a receipt image and select the relevant portions of the image to save your transactions in the db. More features are to be added where you can upload a pdf of your card or bank statement and also chat with your data such that you can gain insights into where your money is going.

The project is under slow development since it is a part time effort. Moreover, since everything is run locally, inference takes a lot of time and hence development is quite slow.

### Demo (current as of 2024-08-12)
> plz no judge ui, ty



## Motivation

I have always wanted a way to track my finances. I am often left wondering where my money is going and while I have a rough idea, I am not sure precisely where my money is going and what I can do to save more. This project is an endevour to remedy that.

## Challenges

1. Working alone.
2. Shit machine.

## Running Instructions

Since this project deals with personal finances, it is meant to be run locally only. It uses [tesseract ocr](https://github.com/tesseract-ocr/tesseract) to decipher images ~and then [llama 3.1](https://ollama.com/library/llama3.1) to interact with data~.

If you are on a mac, clone the repository and simply run `sh ./run.sh` and everything should work out of the box!

If you are on another machine, instructions will be up soon.

## Features

1. Upload an image of a receipt (like grocery bill).
2. Store receipt data in local db.

### Futures

- [ ] Add categorization to the transaction data
- [ ] Draw more boxes on receipt for automatic data filling
- [ ] Train tesseract to better read numbers (and text)
- [ ] Chat with llama about past transactions
- [ ] Upload card and bank statements
- [ ] Improve UI
- [ ] More informative graphs and other dashboard features
- [ ] Personal server, ie, multi device
- [ ] PWA for easy uploads

## Contributing

Feel free to fork this repository, but PRs will likely not be merged. This repo is intended for very personal use and all development will be solely done by me. Of course, do open issues if you notice a bug or want to request a feature.