from dataclasses import dataclass
import heapq 


@dataclass
class Buy:
    volume: int
    price: float

    def _equal_(self, other):
        return self.price == other.price
    def _less_(self, other):
        return self.price > other.price

@dataclass
class SellItem:
    volume: int
    price: float

    def _equal_(self, other):
        return other.price == self.price
    def _less_(self, other):
        return other.price > self.price

class OrderBook:
    def _init_(self):
        self.sell_order = []
        self.buy_order = []

    def processing(self) -> int:
        count = 0
        while self.buy_order and self.sell_order and self.buy_order[0].price >= self.sell_order[0].price:
            sell_o = heapq.heappop(self.sell_order)
            buy_o = heapq.heappop(self.buy_order)
            count += min(buy_o.volume, sell_o.volume)
            if buy_o.volume < sell_o.volume:
                heapq.heappush(self.sell_order, Buy(sell_o.volume -buy_o.volume, sell_o.price))
            elif buy_o.volume >sell_o.volume:
                heapq.heappush(self.buy_order, Buy(buy_o.volume - sell_o.volume, buy_o.price))                
        return count

    def sell(self, volume, price) :
        heapq.heappush(self.sell_q, SellItem(volume, price))
        return self.processing()

    def buy(self, volume, price) :
        heapq.heappush(self.buy_order, Buy(volume, price))
        return self.processing()
