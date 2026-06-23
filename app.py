class BlackjackAdvisor:
    def __init__(self, num_decks=6):
        # A standard deck has 4 of each card, but 16 ten-value cards (10, J, Q, K)
        # 1 represents the Ace (soft/hard logic handled dynamically)
        self.base_deck = {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 16}
        self.shoe = {card: count * num_decks for card, count in self.base_deck.items()}
        
    def remove_cards(self, card_list):
        """Track visible cards dealt on the table to update the live distribution."""
        for card in card_list:
            if self.shoe.get(card, 0) > 0:
                self.shoe[card] -= 1

    def get_hand_value(self, hand):
        """Calculates hand total, optimally managing Ace flexibility (1 or 11)."""
        total = sum(hand)
        # Handle Ace being 11 if it doesn't cause a bust
        if 1 in hand and total + 10 <= 21:
            return total + 10, True  # True means it's a "Soft" hand
        return total, False          # False means it's a "Hard" hand

    def analyze_next_card(self, player_hand, dealer_upcard):
        """Calculates probability distribution and gives a HIT/STAND advice."""
        total_remaining_cards = sum(self.shoe.values())
        if total_remaining_cards == 0:
            return {"Error": "No cards left in shoe."}

        player_total, is_soft = self.get_hand_value(player_hand)
        
        # Calculate individual card probabilities
        probabilities = {card: count / total_remaining_cards for card, count in self.shoe.items()}
        
        # Calculate structural probabilities
        bust_prob = 0.0
        safe_prob = 0.0
        
        for card, prob in probabilities.items():
            # Determine hypothetical new total if this card is drawn
            temp_hand = player_hand + [card]
            new_total, _ = self.get_hand_value(temp_hand)
            
            if new_total > 21:
                bust_prob += prob
            else:
                safe_prob += prob

        # Basic Strategy recommendation logic
        if is_soft:
            action = "HIT" if player_total <= 17 else "STAND"
        else:
            # Hard hand logic vs Dealer Upcard (Fixed missing conditions)
            if player_total <= 11:
                action = "HIT"  
            elif player_total == 12:
                action = "STAND" if dealer_upcard in [4, 5, 6] else "HIT"
            elif 13 <= player_total <= 16:
                action = "STAND" if dealer_upcard in [2, 3, 4, 5, 6] else "HIT"
            else:
                action = "STAND"

        return {
            "Player Total": player_total,
            "Hand Type": "Soft" if is_soft else "Hard",
            "Bust Probability": f"{bust_prob * 100:.2f}%",
            "Safe Card Probability": f"{safe_prob * 100:.2f}%",
            "Recommended Action": action,
            "Live Deck Probs": {k: f"{v*100:.1f}%" for k, v in probabilities.items()}
        }

# --- REAL-TIME GAMEPLAY EXECUTION FIX ---
# 1. Initialize a 6-deck shoe game (standard casino rule)
advisor = BlackjackAdvisor(num_decks=6)

# 2. Burn/Remove initial dead cards from other players (Fixed empty bracket bug)
advisor.remove_cards([10, 5, 7, 2, 9, 10])

# 3. Define Your current Hand and the Dealer's upcard
my_hand = [10, 4]       # Total: Hard 14
dealer_face_up = 7      # Dealer shows a 7

# 4. Remove your hand and dealer's card from the shoe tracker
advisor.remove_cards(my_hand + [dealer_face_up])

# 5. Run the analytics
analysis = advisor.analyze_next_card(my_hand, dealer_face_up)

# Print clean output for evaluation
for key, val in analysis.items():
    if key != "Live Deck Probs":
        print(f"{key}: {val}")
