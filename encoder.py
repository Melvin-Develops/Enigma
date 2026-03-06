import string

class EnigmaMachine:
    def __init__(self, start_pos=(0, 0, 0), plugs=""):
        self.chars = string.ascii_uppercase + string.digits
        self.size = len(self.chars)
        
        # Fixed Scrambled Rotors (The internal wiring)
        self.rotors = [
            "9876543210ZYXWVUTSRQPONMLKJIHGFEDCBA",
            "QWERTYUIOPASDFGHJKLZXCVBNM1234567890",
            "0X1Y2Z3A4B5C6D7E81F9G0HIJKLMNOPQRSTUV"
        ]
    
        self.pos = list(start_pos)
        self.plugboard = self._setup_plugboard(plugs.upper())

    def _setup_plugboard(self, plugs):
        mapping = {c: c for c in self.chars}
        pairs = plugs.split()
        for pair in pairs:
            if len(pair) == 2:
                a, b = pair[0], pair[1]
                mapping[a], mapping[b] = b, a
        return mapping

    def _step_rotors(self):
        self.pos[0] += 1
        if self.pos[0] == self.size:
            self.pos[0] = 0
            self.pos[1] += 1
            if self.pos[1] == self.size:
                self.pos[1] = 0
                self.pos[2] = (self.pos[2] + 1) % self.size

    def _map_char(self, char, rotor_str, pos, reverse=False):
        if reverse:
            shift_idx = (self.chars.find(char) + pos) % self.size
            char_at_shift = self.chars[shift_idx]
            original_idx = (rotor_str.find(char_at_shift) - pos) % self.size
            return self.chars[original_idx]
        else:
            idx = (self.chars.find(char) + pos) % self.size
            scrambled_char = rotor_str[idx]
            result_idx = (self.chars.find(scrambled_char) - pos) % self.size
            return self.chars[result_idx]

    def process(self, text):
        output = ""
        for char in text.upper():
            if char not in self.chars:
                output += char
                continue
            self._step_rotors()
            res = self.plugboard[char]
            for i in range(3):
                res = self._map_char(res, self.rotors[i], self.pos[i])
            ref_idx = self.chars.find(res)
            res = self.chars[-(ref_idx + 1)]
            for i in range(2, -1, -1):
                res = self._map_char(res, self.rotors[i], self.pos[i], reverse=True)
            res = self.plugboard[res]
            output += res
        return output

# --- INTERACTIVE TERMINAL APP ---
def main():
    print("--- DIGITAL ENIGMA SIMULATOR ---")
    
    # 1. Set the Secret Key
    try:
        key_input = input("Enter 3 numbers for the key (e.g., 10 5 22): ")
        key = tuple(map(int, key_input.split()))
    except:
        print("Invalid key format. Using (0,0,0)")
        key = (0,0,0)

    # 2. Set the Plugboard
    plugs = input("Enter plug swaps (e.g., AB 12) or leave blank: ")
    
    # Initialize machine
    enigma = EnigmaMachine(start_pos=key, plugs=plugs)
    
    # 3. Encrypt or Decrypt
    msg = input("Enter message to Process: ")
    result = enigma.process(msg)
    
    print(f"\nRESULT: {result}")
    print("--------------------------------")

if __name__ == "__main__":
    main()