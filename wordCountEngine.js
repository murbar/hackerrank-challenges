/* Word Count Engine - https://www.pramp.com/challenge/W5EJq2Jld3t2ny9jyZXG
Implement a document scanning function wordCountEngine, which receives a string document and returns a list of all unique words in it and their number of occurrences, sorted by the number of occurrences in a descending order. If two or more words have the same count, they should be sorted according to their order in the original sentence. Assume that all letters are in english alphabet. You function should be case-insensitive, so for instance, the words “Perfect” and “perfect” should be considered the same word.

The engine should strip out punctuation (even in the middle of a word) and use whitespaces to separate words.

Analyze the time and space complexities of your solution. Try to optimize for time while keeping a polynomial space complexity.

Examples:

input:  document = "Practice makes perfect. you'll only
                    get Perfect by practice. just practice!"

output: [ ["practice", "3"], ["perfect", "2"],
          ["makes", "1"], ["youll", "1"], ["only", "1"], 
          ["get", "1"], ["by", "1"], ["just", "1"] ]
Important: please convert the occurrence integers in the output list to strings (e.g. "3" instead of 3). We ask this because in compiled languages such as C#, Java, C++, C etc., it’s not straightforward to create mixed-type arrays (as it is, for instance, in scripted languages like JavaScript, Python, Ruby etc.). The expected output will simply be an array of string arrays.
*/

const isLowerAlpha = ch => 'abcdefghijklmnopqrstuvwxyz'.includes(ch);

const parse = word =>
  [...word]
    .map(c => c.toLowerCase())
    .filter(isLowerAlpha)
    .join('');

function wordCountEngine(document) {
  const words = document.split(' ');
  const counts = {};
  const cleaned = words.map(w => parse(w)).filter(w => w.length > 0);
  cleaned.forEach(word => {
    if (word in counts) {
      counts[word] += 1;
    } else {
      counts[word] = 1;
    }
  });
  const noDupes = [...new Set(cleaned)];
  return noDupes
    .map(w => [w, String(counts[w])])
    .sort((a, b) => {
      if (b[1] !== a[1]) return b[1] - a[1];
      aIndex = cleaned.findIndex(w => w === a[0]);
      bIndex = cleaned.findIndex(w => w === b[0]);
      return aIndex - bIndex;
    });
}

console.log(
  wordCountEngine(
    "Practice makes perfect. you'll only get Perfect by practice. just practice!"
  )
);
