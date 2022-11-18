if (piece == "W" and row == 8) or (piece == "B" and row == 1):
                return (8**8 * 16)-state.num_plays if piece_player == piece else -(8**8 * 16)
            # State where win/lost is guaranteed next round