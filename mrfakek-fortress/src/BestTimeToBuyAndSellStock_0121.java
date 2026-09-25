public class BestTimeToBuyAndSellStock_0121 {

    public int maxProfit(int[] prices) {
        int pricesSize = prices.length;
        int bestBuyPrice = prices [0];
        int bestSellPrice = 0;
        int bestSpread = 0;
        int tempSpread;
        int tempBuyPrice = bestBuyPrice;
        int tempSellPrice = bestSellPrice;
        int currentPrice;

        for (int i=1; i<pricesSize; i++){
            currentPrice = prices[i];
            if (currentPrice < tempBuyPrice){
                tempBuyPrice = currentPrice;
                tempSellPrice = tempBuyPrice;
            }
            else if (currentPrice > tempSellPrice){
                tempSellPrice = currentPrice;
                bestSpread = bestSellPrice - bestBuyPrice ;
                tempSpread = tempSellPrice -tempBuyPrice;
                if (bestSpread < tempSpread){
                    bestBuyPrice = tempBuyPrice;
                    bestSellPrice = tempSellPrice;
                    bestSpread = tempSpread;
                }
            }
        }
    return bestSpread;
    }
}
