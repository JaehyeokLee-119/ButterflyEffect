SYSTEM_MESSAGE = """Solve a question answering task with interleaving Thought, Action, Observation steps. Thought can reason about the current situation, and Action can be two types:
(1) Search[entity], which searches the exact entity on Wikipedia and returns the paragraph if it exists. If not, it will return some similar entities to search.
(2) Finish[answer], which returns the answer and finishes the task."""

INSIGHTS = """ 
- Final answer can exactly found at observation or question or ('yes' or 'no').
- Don't use Search[entity] or Finish[answer] action at Thought.
- You must use only Search[entity] or Finish[answer] at Action.
- Search at least two documents before use Finish[answer] action.
- If you could not search document, it is good method which instead searching in similar documents.
- If you use Search[entity], it is bad to use sentence entity, please use simple entity which contains only one object.
- If you use Finish[answer], answer must be exactly copied only in part of observation or question, exclude if answer is 'yes' or 'no'.
- If you think answer is plural form but the search result is singular form, you must use singular form as answer."""

# INSIGHTS = """ 
# - Final answer can exactly found at observation or question or ('yes' or 'no').   
# - If a search result confirms part of the information but not the specific detail needed, use a targeted search query combining the confirmed information with the missing detail. 
# - If the final answer is a person's name or group's name, ensure it matches the most complete and accurate form as found in the search results, including any middle names, additional identifiers, and correct fullname spelling.  
# - If you could not search document, it is good method which instead searching in similar documents.
# - If you use Search[entity], it is bad to use sentence entity, please use simple entity which contains only one object.
# - If you use Finish[answer], answer must be exactly copied only in part of observation or question, exclude if answer is 'yes' or 'no'.
# - If you think answer is plural form but the search result is singular form, you must use singular form as answer.
# - Please at Finish[answer], if answer is human's name, submit his full name as the correct answer. Don't miss the middle name."""

FEWSHOTS = ["""Question: Which is the tallest skyscraper, Manhattan Life Insurance Building or 1717 Broadway?-
Thought 1: I need to search Manhattan Life Insurance Building
Action 1: Search[Manhattan Life Insurance Building]
Observation 1: The Manhattan Life Insurance Building was a 348 ft tower at 64-66 Broadway in New York City completed in 1894 to the designs of the architects of Kimball & Thompson and slightly extended north in 1904 making its new address 64-70 Broadway.  It was the first skyscraper to pass 100 m in Manhattan.
Thought 2: The Manhattan Life Insurance Building is 348 ft tall. I need to search 1717 Broadway next.
Action 2: Search[1717 Broadway]
Observation 2: 1717 Broadway is a skyscraper located in Manhattan, New York City, United States.  At 750 feet high, it is the tallest hotel in North America.  The building contains two hotels, the Courtyard New York Manhattan/Central Park and the Residence Inn New York Manhattan/Central Park, with a total of 639 rooms.  The glass-clad building is located on the Northwest corner of 54th Street and Broadway.
Thought 3: 1717 Broadway is 750 ft tall, which is taller than the Manhattan Life Insurance Building. So the tallest skyscraper is 1717 Broadway.
Action 3: Finish[1717 Broadway]""",
"""Question: Who was the head coach of the 2016 New York Giants?
Thought 1: I need to search about 2016 New York Giants.
Action 1: Search[2016 New York Giants]
Observation 1: Could not find [2016 New York Giants]. Similar: [2016 New York Giants season], [New York Giants], [New York Giants (PL)], [2017 New York Giants season], [2016 San Francisco Giants season]
Thought 2: I couldn't find 2016 New York Giants, so I will search 2016 New York Giants season instead. 
Action 2: Search[2016 New York Giants season]
Observation 2: The 2016 season was the New York Giants' 92nd season in the National Football League, their seventh playing their home games at MetLife Stadium and the first under head coach Ben McAdoo.
Thought 3: The head coach of the 2016 New York Giants was Ben McAdoo. I need to search for Ben McAdoo.
Action 3: Search[Ben McAdoo]
Observation 3: Benjamin Lee "Ben" McAdoo (born July 9, 1977) is an American football coach who is the head coach of the New York Giants of the National Football League (NFL).
Thought 4: The head coach of the 2016 New York Giants was Benjamin Lee "Ben" McAdoo.
Action 4: Finish[Benjamin Lee "Ben" McAdoo]""",
"""Question: Which was built first, the Theodosius Cistern or the German Fountain?
Thought 1: I need to search Theodosius Cistern.
Action 1: Search[Theodosius Cistern]
Observation 1: The Theodosius Cistern (Greek: Κινστέρνα Θεοδοσίου , Turkish: Şerefiye Sarnıcı ) is one of many ancient cisterns of Constantinople that lie beneath the city of Istanbul, Turkey.  The modern entrance is in Piyer Loti Caddesi, Fatih.
Thought 2: The Theodosius Cistern was built in ancient Constantinople. I will search for the German Fountain.
Action 2: Search[German Fountain]
Observation 2: The German Fountain (Turkish: "Alman Çeşmesi" German: "Deutscher Brunnen" ) is a gazebo styled fountain in the northern end of old hippodrome (Sultanahmet Square), Istanbul, Turkey and across from the Mausoleum of Sultan Ahmed I.  It was constructed to commemorate the second anniversary of German Emperor Wilhelm II's visit to Istanbul in 1898.  It was built in Germany, then transported piece by piece and assembled in its current site in 1900.  The neo-Byzantine style fountain's octagonal dome has eight marble columns, and dome's interior is covered with golden mosaics.
Thought 3: The German Fountain was built in 1900 to commemorate the second anniversary of German Emperor Wilhelm II's visit to Istanbul in 1898. Since Theodosius Cistern was built in ancient Constantinople, Theodosius Cistern was built first.
Action 3: Finish[Theodosius Cistern]""",
"""Question:  "The World Is in My Hands" is a song recorded by a German dance music act with an estimated net worth of over how much?
Thought 1: I need to search for "The World Is in My Hands".
Action 1: Search[The World Is in My Hands]
Observation 1: "The World Is in My Hands" is a song written by Yann Peifer, Manuel Reuter and Andres Ballinas and recorded by German dance act Cascada.  The track was confirmed as the third and final single taken from their latest compilation album “The Best of Cascada” that was released on digital retailers on March 29, 2013 via Zooland Records.
Thought 2: The song "The World Is in My Hands" was recorded by German dance act Cascada. I need to find about Cascada.
Action 2: Search[Cascada]
Observation 2: Cascada ( ; Spanish for "Waterfall") is a German dance music act founded in 2004 by singer Natalie Horler, DJ Manian and DJ Yanou.  They are best known for their hit singles "Everytime We Touch", "What Hurts the Most" and "Evacuate the Dancefloor".  Cascada have sold over 30 million albums worldwide, an estimated 15 million digital downloads, and have an estimated net worth of over 7 million.  Cascada represented Germany at the Eurovision Song Contest 2013 in Malmö, Sweden.
Thought 3: Cascada's estimated net worth of over 7 million.
Action 3: Finish[7 million]""",
"""Question: Are The Verve and Richard Ashcroft from the same country?
Thought 1: I need to search The Verve.
Action 1: Search[The Verve]
Observation 1: The Verve were an English rock band formed in Wigan in 1990 by lead vocalist Richard Ashcroft, guitarist Nick McCabe, bass guitarist Simon Jones and drummer Peter Salisbury.  Guitarist and keyboard player Simon Tong later became a member.
Thought 2: The Verve formed in England. I should search for Richard Ashcroft.
Action 2: Search[Richard Ashcroft]
Observation 2: Richard Paul Ashcroft (born 11 September 1971) is an English singer and songwriter.  He was the lead singer and occasional rhythm guitarist of the alternative rock band The Verve from their formation in 1990 until their original split in 1999.  He became a successful solo artist in his own right, releasing three UK top three solo albums.  The Verve reformed in 2007 but again broke up by summer 2009.  Ashcroft then founded a new band, RPA & The United Nations of Sound, and released a new album on 19 July 2010.  On 22 February 2016 Ashcroft announced his fourth solo album, "These People", set for release 20 May 2016.  Chris Martin of Coldplay has described Ashcroft as "the best singer in the world".
Thought 3: Richard Ashcroft is from England. So The Verve and Richard Ashcroft are from the same country.
Action 3: Finish[yes]""",
"""Question: Are eith Nicotiana or Encyclia genus of pine trees?
Thought 1: I need to search Nicotiana.
Action 1: Search[Nicotiana]
Observation 1: Nicotiana ( ) is a genus of herbaceous plants and shrubs of the family Solanaceae, that is indigenous to the Americas, Australia, south west Africa and the South Pacific.  Various "Nicotiana" species, commonly referred to as tobacco plants, are cultivated as ornamental garden plants. " N. tabacum" is grown worldwide for production of tobacco leaf for cigarettes and other tobacco products.
Thought 2: Nicotiana is a genus of herbaceous plants. I need to search Encyclia.
Action 2: Search[Encyclia]
Observation 2: Encyclia is a genus of orchids.  The genus name comes from Greek "enkykleomai" ("to encircle"), referring to the lateral lobes of the lip which encircle the column.  The abbreviation in the horticultural trade is E.
Thought 3: Encyclia is a genus of orchids. Neither Nicotiana nor Encyclia are genus of pine trees.
Action 3: Finish[no]""",
"""Question: How old is the actor who started in the 1957 American drama film, "Old Yeller".
Thought 1: I need to search for the 1957 American drama film, "Old Yeller".
Action 1: Search[1957 American drama film, "Old Yeller"]
Observation 1: Could not find [1957 American drama film, "Old Yeller"]. Similar: [Old Yeller (film)], [List of American films of 1957], [1957 in film], [List of British films of 1957], [List of American films of 1958]
Thought 2: I will search Old Yeller (film).
Action 2: Search[Old Yeller (film)]
Observation 2: Old Yeller is a 1957 American drama film produced by Walt Disney.  It stars Tommy Kirk, Dorothy McGuire and Beverly Washburn.  It is about a boy and a stray dog in post-Civil War Texas.  The film is based upon the 1956 Newbery Honor-winning book of the same name by Fred Gipson.  Gipson also cowrote the screenplay with William Tunberg.  The success of the "Old Yeller" film led to a sequel, "Savage Sam", which was also based on a book by Gipson.
Thought 3: I will search Tommy Kirk.
Action 3: Search[Tommy Kirk]
Observation 3: Thomas Lee "Tommy" Kirk (born December 10, 1941) is an American former actor and later a businessman.  He is best known for his performances in a number of highly popular movies made by Walt Disney Studios such as "Old Yeller", "The Shaggy Dog", "The Swiss Family Robinson" and "The Misadventures of Merlin Jones", as well as beach party movies of the mid 1960s.
Thought 4: Thomas Lee "Tommy" Kirk born December 10, 1941.
Action 4: Finish[born December 10, 1941]""",
"""Question: What do Freedomland U.S.A. and Baychester both have in common?
Thought 1: I need to search for Freedomland U.S.A.
Action 1: Search[Freedomland U.S.A.]
Observation 1: Freedomland U.S.A. (usually called just Freedomland) was a short-lived, American history-themed amusement park in the Baychester area in the northeastern part of the Bronx borough in New York City.  Its slogan was "The World's Largest Entertainment Center" (later, "The World's Largest Outdoor Family Entertainment Center").
Thought 2: Freedomland U.S.A. was located in the Baychester area of the Bronx. I need to verify the location of Baychester.
Action 2: Search[Baychester]
Observation 2: Could not find [Baychester]. Similar: [Lanchester Bay], [Eastchester Bay], [Portchester], [Bedchester], [Baychester, Bronx]
Thought 3: I should search for Baychester, Bronx since Baychester was listed as a similar entity under Bronx.
Action 3: Search[Baychester, Bronx]
Observation 3: Baychester is dominated by one and two family homes of various styles.  The total land area is 2.61 square miles.  The area is low laying and flat; some parts of the East Bronx are built on marshland and valleys.  The area was formerly home to the amusement park Freedomland U.S.A., opened in 1959 and closed in 1964.
Thought 4: Both  Freedomland U.S.A and Baychester was formerly home to the amusement park.
Action 4: Finish[formerly home to the amusement park]""",
"""Question: Who is the head of state of Germany who commanded the SM UC-25 minelaying submarine ?
Thought 1: I need to find SM UC-25.
Action 1: Search[SM UC-25]
Observation 1: SM "UC-25" was a German Type UC II minelaying submarine or U-boat in the German Imperial Navy (German: "Kaiserliche Marine" ) during World War I.  The U-boat was ordered on 29 August 1915 and was launched on 10 June 1916.  She was commissioned into the German Imperial Navy on 28 June 1916 as SM "UC-25".  In 13 patrols "UC-25" was credited with sinking 21 ships, either by torpedo or by mines laid.  March–September 1918 she was commanded by Karl Dönitz, later Grand admiral.  "UC-25" was scuttled at Pola on 28 October 1918 on the surrender of Austria-Hungary.
Thought 2: SM "UC-25" was commanded by Karl Dönitz. I need to search Karl Dönitz.
Action 2: Search[Karl Dönitz]
Observation 2: Karl Dönitz (sometimes spelt Doenitz) (] ; 16 September 1891 – 24 December 1980) was a German admiral who played a major role in the naval history of World War II.  Dönitz briefly succeeded Adolf Hitler as the head of state of Germany.
Thought 3: The head of state of Germany who commanded the SM UC-25 minelaying submarine was Karl Dönitz.
Action 3: Finish[Karl Dönitz]""",
"""Question: What is the name of this town located on the larger of the two Fox Islands in Maine, where Philip Jamison's summer home is located?
Thought 1: I need to search for Fox Islands in Maine.
Action 1: Search[Fox Islands Maine]
Observation 1: Could not find [Fox Islands Maine]. Similar: [Fox Islands (Alaska)], [Fox Islands (Michigan)], [Island fox], [Fox Island, South Coast, Newfoundland and Labrador], [Fox Island (Rhode Island)]
Thought 2: The search results are not helpful. I should search for where Philip Jamison's summer home.
Action 2: Search[Philip Jamison's summer home]
Observation 2: Could not find [Philip Jamison's summer home]. Similar: [Philip Jamison], [Robert Jamison], [Little Jamison, California], [John Jamison], [Jamison (surname)]
Thought 3: I will search Philip Jamison.
Action 3: Search[Philip Jamison]
Observation 3: Philip Jamison is an artist working primarily with watercolour as a medium.  Jamison's inspiration comes mainly from the environs of his home in West Chester, Pennsylvania, and his summer home in Vinalhaven, Maine; typical scenes are landscapes, seascapes, interiors and flower arrangements.  The daisy flower was Jamison's particular favorite.
Thought 4: Philip Jamison's summer home is located in Vinalhaven, Maine.
Action 4: Finish[Vinalhaven, Maine]"""]