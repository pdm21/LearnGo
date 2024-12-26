package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"

	"github.com/PuerkitoBio/goquery"
)

func fetchStockPrice(symbol string) (string, error) {
	// construct the Yahoo Finance URL, based off of patterns
	url := fmt.Sprintf("https://finance.yahoo.com/quote/%s", symbol)

	// HTTP GET request to fetch the webpage, and then defer to free up resources
	resp, err := http.Get(url)
	if err != nil {
		return "", fmt.Errorf("failed to fetch stock data: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("received non-200 response code: %d", resp.StatusCode)
	}

	// Parse the HTML
	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to parse HTML: %v", err)
	}

	// Find the stock price in the `fin-streamer` tag with `data-field="postMarketPrice"`
	price := doc.Find(`fin-streamer[data-field="postMarketPrice"]`).AttrOr("data-value", "")
	if price == "" {
		return "", fmt.Errorf("could not find stock price on the page")
	}

	return price, nil
}

func main() {
	// Define a flag for the stock symbol
	symbol := flag.String("symbol", "", "Stock symbol to fetch the price for")
	flag.Parse()

	// Validate input
	if *symbol == "" {
		log.Fatal("Please provide a stock symbol using the -symbol flag")
	}

	// Fetch the stock price
	price, err := fetchStockPrice(*symbol)
	if err != nil {
		log.Fatalf("Error fetching stock price for %s: %v", *symbol, err)
	}

	// Print the stock price
	fmt.Printf("The current price of %s is: %s\n", *symbol, price)
}
