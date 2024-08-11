# Localhost Expense Tracker

This project is to manage personal finances. Currently, it is really simple in that you upload a receipt image and select the relevant portions of the image to save your transactions in the db. More features are to be added where you can upload a pdf of your card or bank statement and also chat with your data such that you can gain insights into where your money is going.

The project is under slow development since it is a part time effort. Moreover, since everything is run locally, inference takes a lot of time and hence development is quite slow.

## Motivation

I have always wanted a way to track my finances. I am often left wondering where my money is going and while I have a rough idea, I am not sure precisely where my money is going and what I can do to save more. This project is an endevour to remedy that.

## Running Instructions

Since this project deals with personal finances, it is meant to be run locally only. It uses [tesseract ocr](https://github.com/tesseract-ocr/tesseract) to decipher images and then [llama 3.1](https://ollama.com/library/llama3.1) to interact with data.

> Instructions todo

## Features

1. Upload an image of a receipt (like grocery bill) and store transactions in db.
> see futures below

### Futures

- [ ] Chat with llama about past transactions
- [ ] Upload card and bank statements
- [ ] More informative graphs and other dashboard features