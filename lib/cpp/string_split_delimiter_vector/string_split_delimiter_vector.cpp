// Function to split a string based on a char delimiter, and place parts in a string vector
//  @ output vector<string>
//  @ input string str: string to be split
//  @ input char delimiter  
vector<string> split(string str, char delimiter) {
  vector<string> internal;
  stringstream ss(str); // Turn the string into a stream.
  string tok;
  while(getline(ss, tok, delimiter)) {
    internal.push_back(tok);
  }
  return internal;
}
