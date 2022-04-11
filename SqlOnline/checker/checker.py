#!/usr/bin/env python3

import sys
import requests
import enum
import typing
import random
import json
import string
import re
import json_tools

PORT = 8000
names = ('Aaberg', 'Abbot', 'Abernon', 'Abram', 'Ackerley', 'Adalbert', 'Adamsen', 'Ade', 'Ader', 'Adlare', 'Adore', 'Adrienne', 'Afton', 'Agle', 'Ahab', 'Aida', 'Ailyn', 'Ajay', 'Alabaster', 'Alarise', 'Albertine', 'Alcott', 'Aldric', 'Alejoa', 'Alexandr', 'Alfons', 'Alice', 'Alisia', 'Allare', 'Allina', 'Allys', 'Aloise', 'Alrich', 'Alva', 'Alwin', 'Amadas', 'Amand', 'Amasa', 'Ambrosia', 'Amethist', 'Ammann', 'Ana', 'Anastice', 'Anderegg', 'Andres', 'Anet', 'Angelita', 'Anissa', 'Annabelle', 'Annie', 'Anselmo', 'Antone', 'Anzovin', 'Aprilette', 'Arbe', 'Ardehs', 'Ardrey', 'Argyle', 'Arielle', 'Arleyne', 'Armando', 'Arnelle', 'Arratoon', 'Artima', 'Arvonio', 'Asher', 'Ashraf', 'Astraea', 'Athal', 'Atrice', 'Auberon', 'Audra', 'Augusta', 'Aurelius', 'Autry', 'Avictor', 'Axe', 'Aziza', 'Bachman', 'Baiel', 'Bakki', 'Ballard', 'Bander', 'Bar', 'Barbi', 'Barimah', 'Barnie', 'Barry', 'Bartley', 'Bashuk', 'Batha', 'Baudoin', 'Bayly', 'Beasley', 'Beberg', 'Beeck', 'Behrens', 'Belayneh', 'Belle', 'Bendicta', 'Benil', 'Bennink', 'Berardo', 'Bergmann', 'Berlauda', 'Bernelle', 'Berry', 'Bertolde', 'Bethel', 'Betty', 'Bevis', 'Bible', 'Bigod', 'Bilow', 'Birdie', 'Bixby', 'Blakelee', 'Blaseio', 'Blithe', 'Bluhm', 'Bobbette', 'Boehmer', 'Bohman', 'Bollen', 'Bonina', 'Booker', 'Borden', 'Borreri', 'Boucher', 'Bowden', 'Boycie', 'Brackett', 'Braeunig', 'Brandie', 'Braunstein', 'Breen', 'Brenna', 'Briana', 'Brietta', 'Bringhurst', 'Brittany', 'Broder', 'Bronnie', 'Brott', 'Brunella', 'Bryner', 'Buckley', 'Buffy', 'Bum', 'Burchett', 'Burkley', 'Burny', 'Busby', 'Butte', 'Byrom', 'Cadmarr', 'Caitrin', 'Calia', 'Calloway', 'Camel', 'Campbell', 'Candyce', 'Caplan', 'Carbone', 'Cargian', 'Carlen', 'Carlstrom', 'Carmencita', 'Carolina', 'Carrick', 'Cary', 'Casimire', 'Cassondra', 'Catha', 'Catima', 'Cavanagh', 'Ceciley', 'Celestyn', 'Centonze', 'Chace', 'Chak', 'Chandless', 'Chapman', 'Charla', 'Charmion', 'Chavaree', 'Chema', 'Cherice', 'Chesney', 'Chickie', 'Chiou', 'Chon', 'Christalle', 'Christis', 'Chu', 'Ciapha', 'Cinda', 'Cirone', 'Clarabelle', 'Clarisse', 'Claudio', 'Clein', 'Cleodal', 'Cliff', 'Close', 'Cnut', 'Codee', 'Cohe', 'Colburn', 'Collen', 'Colpin', 'Combe', 'Conchita', 'Conner', 'Constant', 'Cooley', 'Corabelle', 'Cordie', 'Corin', 'Cornelie', 'Corrinne', 'Cosetta', 'Cottrell', 'Covell', 'Craggy', 'Crean', 'Cressler', 'Cristian', 'Crompton', 'Cruickshank', 'Culliton', 'Currey', 'Cutlip', 'Cynara', 'Cyril', 'Dael', 'Dahlstrom', 'Dallis', 'Dambro', 'Danczyk', 'Daniell', 'Dante', 'Darby', 'Darice', 'Darrelle', 'Dasha', 'Davey', 'Dawn', 'Dearborn', 'Decato', 'Deedee', 'Dela', 'Delija', 'Delos', 'Deming', 'Denie', 'Denver', 'Dermot', 'Des', 'Deste', 'Devland', 'Dewitt', 'Dianemarie', 'Dich', 'Dielle', 'Dimitri', 'Dinsmore', 'Dittman', 'Docile', 'Doi', 'Dolphin', 'Dominus', 'Donela', 'Donny', 'Dorcus', 'Dorinda', 'Dorothi', 'Dosi', 'Douglas', 'Downs', 'Dream', 'Driskill', 'Drummond', 'Dudden', 'Dulcia', 'Dunham', 'Durant', 'Durward', 'Duvall', 'Dyanne', 'Eachelle', 'Earley', 'Ebby', 'Eckart', 'Edea', 'Edina', 'Edmonds', 'Edva', 'Egarton', 'Ehrlich', 'Eisenstark', 'Elberta', 'Eldreeda', 'Eleph', 'Eliathan', 'Elish', 'Ellerd', 'Ellora', 'Elnore', 'Elsie', 'Elvis', 'Emalia', 'Emersen', 'Emmalee', 'Emmuela', 'Eng', 'Ennis', 'Ephrayim', 'Erastus', 'Erica', 'Erland', 'Ermine', 'Erroll', 'Esma', 'Estell', 'Ethan', 'Etoile', 'Eugene', 'Euphemie', 'Evander', 'Evelyn', 'Evslin', 'Ezana', 'Fabio', 'Fadil', 'Fairman', 'Fanchon', 'Fari', 'Farny', 'Fasano', 'Faus', 'Fawnia', 'Fedak', 'Feldt', 'Feliza', 'Fenner', 'Feriga', 'Ferrel', 'Fia', 'Fiertz', 'Fillander', 'Fini', 'Firman', 'Fitzpatrick', 'Fleeman', 'Flip', 'Florin', 'Flss', 'Fonsie', 'Forras', 'Foskett', 'France', 'Francoise', 'Franz', 'Freda', 'Fredette', 'French', 'Friedberg', 'Frodeen', 'Fruma', 'Fullerton', 'Fusco', 'Gabrielle', 'Gahan', 'Galatia', 'Gamali', 'Garaway', 'Gare', 'Garlen', 'Garris', 'Gaspar', 'Gauldin', 'Gavrielle', 'Gayner', 'Gefen', 'Gemina', 'Genisia', 'Geoffry', 'Georglana', 'Gerfen', 'Germana', 'Gerstner', 'Gherardi', 'Gibb', 'Giesser', 'Gilberto', 'Gill', 'Gilmore', 'Ginny', 'Girardi', 'Giuditta', 'Gladis', 'Glenda', 'Glover', 'Godber', 'Goer', 'Goldin', 'Gomar', 'Goodden', 'Gordie', 'Gotcher', 'Gow', 'Graham', 'Granny', 'Graybill', 'Greenstein', 'Gregory', 'Greyso', 'Grimbald', 'Groark', 'Grosvenor', 'Gualterio', 'Guild', 'Gunilla', 'Gusba', 'Guthrey', 'Gwenora', 'Hachmann', 'Haerle', 'Haile', 'Haldane', 'Hall', 'Halpern', 'Hamid', 'Hamrnand', 'Hankins', 'Hanser', 'Hardan', 'Harim', 'Harms', 'Harriette', 'Hartmunn', 'Hasheem', 'Hatfield', 'Havener', 'Hayman', 'Hazen', 'Hebert', 'Hedvah', 'Heidie', 'Heise', 'Helenka', 'Helsie', 'Hendry', 'Henricks', 'Hepsiba', 'Hermann', 'Herrah', 'Hertz', 'Hess', 'Hewie', 'Hidie', 'Hilary', 'Hillegass', 'Hime', 'Hiroshi', 'Hoashis', 'Hoem', 'Hola', 'Hollinger', 'Holtorf', 'Honora', 'Horacio', 'Hortense', 'Hound', 'Howlond', 'Huberman', 'Hufnagel', 'Hulen', 'Hun', 'Hurless', 'Hutchinson', 'Hyde', 'Iaria', 'Idel', 'Ieso', 'Ihab', 'Ilise', 'Imelda', 'Infeld', 'Ingold', 'Iny', 'Iphigeniah', 'Irmina', 'Isac', 'Isidora', 'Israel', 'Ive', 'Iz', 'Jacie', 'Jacoba', 'Jacquette', 'Jaffe', 'Jala', 'Jamison', 'Janelle', 'Janis', 'Janyte', 'Jariah', 'Jarvis', 'Jaye', 'Jeanna', 'Jeffcott', 'Jehovah', 'Jen', 'Jennee', 'Jerad', 'Jerol', 'Jesher', 'Jeth', 'Jillana', 'JoAnne', 'Jobe', 'Jody', 'Johanan', 'Johns', 'Jolenta', 'Jones', 'Jordon', 'Joselow', 'Josselyn', 'Jozef', 'Judus', 'Julie', 'Juni', 'Justine', 'Kaela', 'Kaitlynn', 'Kalin', 'Kama', 'Kania', 'Karas', 'Karissa', 'Karlyn', 'Kary', 'Kassity', 'Katheryn', 'Katonah', 'Kaufmann', 'Kaz', 'Keeler', 'Keiko', 'Kelila', 'Kelsy', 'Kendrah', 'Kenneth', 'Kenwee', 'Kerman', 'Kery', 'Kevin', 'Khichabia', 'Kieran', 'Killian', 'Kimmel', 'Kingston', 'Kira', 'Kirsteni', 'Kitty', 'Klement', 'Klos', 'Knowle', 'Kobylak', 'Kolk', 'Konstantine', 'Korenblat', 'Kosel', 'Kowtko', 'Krause', 'Krenn', 'Kristel', 'Krock', 'Krystalle', 'Kumler', 'Kusin', 'Kyla', 'LaMee', 'Lachman', 'Lahey', 'Lali', 'Lammond', 'Lancelot', 'Landry', 'Langston', 'Laraine', 'Larkin', 'Lashondra', 'Latimer', 'Latt', 'Launcelot', 'Lauretta', 'Lavena', 'Lawson', 'LeMay', 'Leanora', 'Leclair', 'Leesen', 'Leid', 'Lela', 'Lemon', 'Lenno', 'Leon', 'Leontina', 'Leshia', 'Letizia', 'Leveridge', 'Lewellen', 'Lezlie', 'Libby', 'Lidia', 'Lila', 'Lily', 'Lindbom', 'Lindy', 'Linnie', 'Lipscomb', 'Liss', 'Liu', 'Lizzy', 'Lodmilla', 'Lolande', 'Longan', 'Lopes', 'Lorena', 'Lorinda', 'Lorry', 'Lotus', 'Loux', 'Lowney', 'Lubeck', 'Lucic', 'Lucy', 'Luelle', 'Lulita', 'Lunneta', 'Lustick', 'Lyford', 'Lynelle', 'Lysander', 'MacGregor', 'Maccarone', 'Macy', 'Madelaine', 'Madonia', 'Magda', 'Magna', 'Mahon', 'Maire', 'Malamud', 'Malia', 'Mallis', 'Malvie', 'Mandi', 'Manny', 'Manya', 'Marcellina', 'Marcoux', 'Margalo', 'Margit', 'Mariano', 'Marigolde', 'Marion', 'Market', 'Marler', 'Maro', 'Marrissa', 'Martelli', 'Martinson', 'Marya', 'Marysa', 'Mastic', 'Mathian', 'Matthaus', 'Maud', 'Maurili', 'Maxentia', 'Mayce', 'Mazonson', 'McClelland', 'McCullough', 'McGraw', 'McKinney', 'McNeely', 'Meaghan', 'Medora', 'Meghan', 'Mela', 'Melessa', 'Mella', 'Melody', 'Mendelsohn', 'Meraree', 'Meredi', 'Merlin', 'Merrill', 'Meta', 'Micaela', 'Michelina', 'Middendorf', 'Mikael', 'Milburr', 'Millar', 'Milon', 'Miner', 'Minta', 'Mirilla', 'Mitinger', 'Modeste', 'Mohr', 'Molly', 'Monika', 'Monteith', 'Mord', 'Morganne', 'Morra', 'Mosa', 'Mossman', 'Moyna', 'Mulcahy', 'Munford', 'Murdock', 'Muslim', 'Myra', 'Naamana', 'Nadean', 'Nahshu', 'Names', 'Nanny', 'Nari', 'Natal', 'Nathanial', 'Nazar', 'Neddy', 'Neile', 'Nellir', 'Neri', 'Nessie', 'Neumark', 'Newby', 'Niall', 'Nicki', 'Nicolella', 'Nightingale', 'Nikos', 'Niobe', 'Noach', 'Noell', 'Nollie', 'Nord', 'Normi', 'Norvell', 'Nozicka', 'Nyhagen', 'Obau', 'Obrien', 'Odele', 'Odom', 'Ogg', 'Olatha', 'Olga', 'Olly', 'Olympe', 'Ondine', 'Oona', 'Orbadiah', 'Orgell', 'Orlando', 'Ornstead', 'Orthman', 'Osborn', 'Ossie', 'Othelia', 'Otto', 'Ozzie', "O'Meara", 'Packer', 'Paige', 'Palma', 'Panayiotis', 'Paola', 'Pardoes', 'Parrish', 'Pascale', 'Patience', 'Patterman', 'Paulita', 'Paxton', 'Pearlman', 'Pedroza', 'Pelaga', 'Pena', 'Pentha', 'Per', 'Perloff', 'Perseus', 'Peterson', 'Petronilla', 'Pfeifer', 'Phene', 'Philine', 'Phillis', 'Phox', 'Piefer', 'Pike', 'Pinter', 'Piselli', 'Plante', 'Plumbo', 'Polito', 'Pomona', 'Popelka', 'Portwine', 'Power', 'Prendergast', 'Priebe', 'Prissie', 'Proudfoot', 'Pryor', 'Pulcheria', 'Puto', 'Queenie', 'Quince', 'Quiteris', 'Rachel', 'Radloff', 'Raffaello', 'Rahr', 'Rakia', 'Ramey', 'Randal', 'Ranit', 'Rapp', 'Ratib', 'Ray', 'Rayshell', 'Rebbecca', 'Redfield', 'Reeva', 'Reiche', 'Reinhard', 'Rem', 'Rene', 'Renwick', 'Reuven', 'Rhea', 'Rhodie', 'Ribble', 'Richela', 'Ricker', 'Riegel', 'Riki', 'Rintoul', 'Ritchie', 'Roana', 'Robert', 'Robyn', 'Rockie', 'Rodie', 'Roer', 'Rolando', 'Romanas', 'Romonda', 'Ronny', 'Rosa', 'Rosanne', 'Rosemare', 'Rosenthal', 'Rossen', 'Rothwell', 'Rowney', 'Roz', 'Ruberta', 'Rudin', 'Rufford', 'Ruperta', 'Russo', 'Ruthy', 'Saba', 'Sachi', 'Sadler', 'Saied', 'Salas', 'Sallee', 'Salvador', 'Sami', 'Sanborne', 'Sandry', 'Santa', 'Sarajane', 'Sartin', 'Saum', 'Savior', 'Saylor', 'Schaeffer', 'Scheider', 'Schlesinger', 'Schoening', 'Schriever', 'Schwartz', 'Scotti', 'Seaden', 'Sebastiano', 'Seem', 'Seiter', 'Selhorst', 'Selmner', 'Seow', 'Sergius', 'Seto', 'Seymour', 'Shakti', 'Shanie', 'Shargel', 'Shaughnessy', 'Shear', 'Shel', 'Shelton', 'Shere', 'Sherr', 'Sheya', 'Shippee', 'Shoifet', 'Shue', 'Shute', 'Sibley', 'Sidon', 'Siesser', 'Sik', 'Silsby', 'Simah', 'Sinclair', 'Sirotek', 'Skantze', 'Skipton', 'Slayton', 'Smart', 'So', 'Solberg', 'Sommer', 'Sophey', 'Sosna', 'Spalla', 'Spence', 'Spohr', 'Stacey', 'Stan', 'Stanton', 'Staten', 'Steele', 'Steinke', 'Stephenie', 'Stevena', 'Stillas', 'Stoecker', 'Stouffer', 'Streetman', 'Stroup', 'Stutsman', 'Sugihara', 'Sunda', 'Susana', 'Suzan', 'Swamy', 'Swetlana', 'Sybille', 'Synn', 'Tace', 'Taggart', 'Talbert', 'Tam', 'Tammie', 'Tannenbaum', 'Tarr', 'Tate', 'Tawney', 'Tedda', 'Tegan', 'Ten', 'Terbecki', 'Terrance', 'Tertia', 'Tews', 'Thanh', 'Thedrick', 'Therese', 'Thibaut', 'Thomajan', 'Thorma', 'Three', 'Tibbitts', 'Tiertza')
db_names = ('attache', 'backpack', 'bag', 'baggage', 'barrel', 'basin', 'basket', 'beaker', 'bin', 'bottle', 'bowl', 'box', 'briefcase', 'bucket', 'cabinet', 'can', 'canister', 'canteen', 'carrier', 'carton', 'cask', 'casket', 'chest', 'coffer', 'container', 'cooler', 'crate', 'cube', 'drawer', 'drum', 'flask', 'folder', 'glass', 'holder', 'hutch', 'jar', 'jug', 'locker', 'luggage', 'packet', 'pan', 'plate', 'pocket', 'pod', 'pot', 'pouch', 'purse', 'rack', 'sack', 'satchel', 'suitcase', 'tin', 'tote', 'trunk', 'tray', 'tub', 'tube', 'urn', 'vase', 'vault', 'vial', 'main', 'bookcase', 'bookshelf', 'buffet', 'bureau', 'cabinet', 'chest', 'credenza', 'sideboard', 'altitude', 'archipelago', 'area', 'atlas', 'atoll', 'azimuth', 'bay', 'border', 'butte', 'canal', 'canyon', 'cape', 'capital', 'cave', 'channel', 'chart', 'city', 'cliff', 'compass', 'continent', 'contour', 'country', 'cove', 'degree', 'delta', 'desert', 'dune', 'east', 'elevation', 'equator', 'estuary', 'fjord', 'geyser', 'glacier', 'globe', 'gulf', 'hill', 'island', 'lagoon', 'lake', 'land', 'landform', 'latitude', 'legend', 'longitude', 'map', 'marsh', 'meridian', 'mesa', 'mountain', 'nation', 'north', 'oasis', 'ocean', 'parallel', 'peak', 'peninsula', 'plain', 'plateau', 'pole', 'pond', 'prairie', 'projection', 'reef', 'region', 'reservoir', 'river', 'scale', 'sea', 'sound', 'source', 'south', 'strait', 'swamp', 'territory', 'tributary', 'tropics', 'tundra', 'valley', 'volcano', 'waterfall', 'west', 'wetland', 'world')
descriptions = ('bagel', 'BLT', 'bowl', 'burger', 'burrito', 'cheeseburger', 'cheesesteak', 'clubhouse', 'donut', 'finger', 'frank', 'fries', 'hamburger', 'hoagie', 'hot', 'dog', 'melt', 'muffin', 'nugget', 'panini', 'philly', 'pita', 'pretzel', 'reuben', 'roll', 'sandwich', 'slider', 'sub', 'taco', 'wrap', 'aroma', 'bagel', 'batter', 'beans', 'beer', 'biscuit', 'bread', 'broth', 'burger', 'burrito', 'butter', 'cake', 'candy', 'caramel', 'caviar', 'cheese', 'chili', 'chimichanga', 'chocolate', 'cider', 'cobbler', 'cocoa', 'coffee', 'cookie', 'cream', 'croissant', 'crumble', 'cuisine', 'curd', 'dessert', 'dish', 'drink', 'eggs', 'empanada', 'enchilada', 'entree', 'filet', 'fish', 'flour', 'foie', 'gras', 'food', 'glaze', 'grill', 'hamburger', 'ice', 'juice', 'ketchup', 'kitchen', 'lard', 'liquor', 'margarine', 'marinade', 'mayo', 'mayonnaise', 'meat', 'milk', 'mousse', 'muffin', 'mushroom', 'noodle', 'nut', 'oil', 'olive', 'omelette', 'pan', 'pasta', 'paste', 'pastry', 'pie', 'pizza', 'plate', 'pot', 'poutine', 'pudding', 'queso', 'raclette', 'recipe', 'rice', 'salad', 'salsa', 'sandwich', 'sauce', 'seasoning', 'skillet', 'soda', 'sopapillas', 'soup', 'soy', 'spice', 'steak', 'stew', 'syrup', 'taco', 'taquito', 'tartar', 'taste', 'tea', 'toast', 'tostada', 'vinegar', 'waffle', 'water', 'wheat', 'wine', 'wok', 'yeast', 'yogurt')
table_names = ('array', 'bag', 'bin', 'buffer', 'container', 'deque', 'dictionary', 'field', 'graph', 'hash', 'heap', 'image', 'list', 'map', 'matrix', 'octree', 'quadtree', 'queue', 'record', 'stack', 'string', 'tree', 'trie', 'vector', 'zipper', 'adventure', 'animation', 'bind', 'bot', 'burst', 'camp', 'clan', 'class', 'cockpit', 'combat', 'flag', 'flight', 'game', 'geometry', 'grenade', 'gun', 'horror', 'HUD', 'lag', 'level', 'map', 'model', 'particle', 'plasma', 'platform', 'player', 'points', 'polygon', 'rail', 'reward', 'rocket', 'scene', 'score', 'skill', 'spam', 'sport', 'squad', 'strategy', 'tactics', 'team', 'texture', 'twitch', 'vehicle', 'weapon', 'app', 'artifact', 'bug', 'build', 'client', 'code', 'command', 'container', 'data', 'event', 'expression', 'function', 'input', 'loop', 'object', 'output', 'program', 'server', 'variable', 'alert', 'align', 'app', 'area', 'buffer', 'bug', 'button', 'chart', 'click', 'debug', 'document', 'domain', 'download', 'dynamic', 'embed', 'error', 'event', 'exception', 'fixed', 'float', 'fork', 'frame', 'gallery', 'git', 'graph', 'grid', 'host', 'inline', 'interval', 'keyword', 'load', 'mirror', 'modal', 'module', 'monitor', 'object', 'page', 'popup', 'prefix', 'profile', 'property', 'refresh', 'reload', 'script', 'search', 'shim', 'source', 'static', 'stream', 'sync', 'tab', 'tap', 'timer', 'title', 'touch', 'traffic', 'transfer', 'upload', 'url', 'valid', 'wire')
column_names = ('alpha', 'ambient', 'array', 'atmosphere', 'attenuation', 'biped', 'birth', 'body', 'bone', 'bounce', 'bucket', 'buffer', 'cage', 'camera', 'clip', 'cloth', 'collision', 'color', 'cone', 'cube', 'curve', 'cylinder', 'death', 'depth', 'diffuse', 'distance', 'dope', 'draft', 'edge', 'falloff', 'fire', 'flow', 'fluid', 'font', 'force', 'frame', 'fur', 'geometry', 'ghost', 'graph', 'gravity', 'hair', 'helper', 'highlight', 'horizon', 'hull', 'image', 'intensity', 'integrator', 'keyframe', 'lamp', 'lattice', 'lens', 'lerp', 'life', 'light', 'lighting', 'logic', 'loop', 'map', 'material', 'mesh', 'metaball', 'model', 'motion', 'node', 'object', 'occlusion', 'particle', 'pass', 'path', 'pipeline', 'pixel', 'point', 'polygon', 'prism', 'radiosity', 'ragdoll', 'ray', 'reflection', 'render', 'rig', 'rotation', 'sample', 'scan', 'scene', 'script', 'shader', 'shadow', 'shape', 'shine', 'simulation', 'skeleton', 'sky', 'smoke', 'specular', 'speed', 'sphere', 'spline', 'spot', 'surface', 'tangent', 'teapot', 'text', 'texture', 'torus', 'tracking', 'transform', 'tube', 'unit', 'velocity', 'vertex', 'voxel', 'world', 'adversary', 'algorithm', 'alphabet', 'ancestor', 'array', 'automaton', 'bag', 'bintree', 'bisector', 'block', 'bound', 'branch', 'bridge', 'bucket', 'capacity', 'centroid', 'certificate', 'chain', 'child', 'circuit', 'clique', 'collision', 'combination', 'complexity', 'configuration', 'conjunction', 'cut', 'cycle', 'degree', 'depth', 'deque', 'diameter', 'dictionary', 'digraph', 'distance', 'edge', 'exponential', 'factor', 'factorial', 'flow', 'forest', 'fractal', 'function', 'graph', 'grid', 'hash', 'head', 'heap', 'height', 'interval', 'iteration', 'language', 'leaf', 'link', 'list', 'matrix', 'mean', 'median', 'mode', 'model', 'node', 'negation', 'octree', 'occurrence', 'parent', 'path', 'pattern', 'permutation', 'performance', 'pointer', 'polytope', 'poset', 'predicate', 'prefix', 'quadtree', 'queue', 'radix', 'recursion', 'recurrence', 'reduction', 'relation', 'relaxation', 'root', 'rotation', 'sort', 'sequence', 'sum', 'segment', 'sink', 'stack', 'string', 'suffix', 'tail', 'tournament', 'tree', 'trie', 'vertex', 'weight')

def get_random_name():
    ran = len(names)
    name = names[random.randint(0, ran - 1)]
    return name + str(random.randint(10000, 99999))

def get_random_word():
    try:
        r = requests.get("")
        if r.status_code != 200:
            return random.choice(column_names) + " " + random.choice(db_names)
    except:
        return random.choice(column_names) + " " + random.choice(db_names)
    words = r.text.splitlines()
    return random.choice(words)

def get_password():
    password = []
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(characters)
    for i in range(20):
        password.append(random.choice(characters))
    random.shuffle(password)
    return "".join(password)

def get_json(response, validate_response=True):
    try:
        data = json.loads(response.text)
    except:
        cquit(Status.MUMBLE, f'JSON validation error on url: {response.url}',f'JSON validation error on url: {response.url}, content: {response.text}')
    if not validate_response:
        return data
    try:
        if data["success"] == True:
            return data
        else:
            cquit(Status.MUMBLE, f'Response status not success on url: {response.url}',f'Response status not success on url: {response.url}, content: {response.text}')
    except:
        cquit(Status.MUMBLE, f'Unknown response status ("success" field in response not found), url: {response.url}',f'Unknown response status ("success" field in response not found), url: {response.url}, content: {response.text}')

def check_status_code(response):
    if response.status_code != 200:
        cquit(Status.MUMBLE, f'Code {response.status_code} on url: {response.url}')
    return True

class Status(enum.Enum):
    OK = 101
    CORRUPT = 102
    MUMBLE = 103
    DOWN = 104
    ERROR = 110

    def __bool__(self):
        return self.value == Status.OK


def cquit(status: Status, public: str='', private: typing.Optional[str] = None):
    if private is None:
        private = public

    print(public, file=sys.stdout)
    print(private, file=sys.stderr)
    assert (type(status) == Status)
    sys.exit(status.value)


def check(host):
    # APP check
    # Connect 

    r = requests.get(f'http://{host}:{PORT}/')
    check_status_code(r)

    creds = {"login":get_random_name(),"password":get_password()}

    # Register

    r = requests.post(f'http://{host}:{PORT}/register', json=creds)
    check_status_code(r)
    data = get_json(r)

    # Login
    
    r = requests.post(f'http://{host}:{PORT}/login', json=creds)
    check_status_code(r)
    data = get_json(r)

    try:
        token = data["data"]["jwt"]
    except:
        cquit(Status.MUMBLE, f'Can not get auth token: {r.url}',f'Can not get auth token: {r.url}, content: {r.text}')
    
    auth_header = {'Authorization': f'Bearer {token}'}

    # Getting api key

    r = requests.get(f'http://{host}:{PORT}/api_key', headers=auth_header)
    check_status_code(r)
    data = get_json(r)

    try:
        api_key = data["data"]["apikey"]
    except:
        cquit(Status.MUMBLE, f'Can not get api key: {r.url}',f'Can not get api key: {r.url}, content: {r.text}')

    schema = {
        "name":random.choice(db_names),
        "description":random.choice(descriptions),
        "tables":[
            {
                "tableName":random.choice(table_names) + str(random.randint(100, 999)),
                "columns":[
                    {
                    "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                    "varType":"TEXT"
                    },
                    {
                    "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                    "varType":"TEXT"
                    }
                ]
            },
            {
                "tableName":random.choice(table_names) + str(random.randint(100, 999)),
                "columns":[
                    {
                    "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                    "varType":"INTEGER"
                    },
                    {
                    "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                    "varType":"TEXT"
                    },
                    {
                    "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                    "varType":"TEXT"
                    }
                ]
            }
        ]
    }

    # Creating new database

    r = requests.post(f'http://{host}:{PORT}/new_db', headers=auth_header, json=schema)
    check_status_code(r)
    data = get_json(r)

    # Checking last log

    r = requests.get(f'http://{host}:{PORT}/last_log', params={'seconds': 10})
    check_status_code(r)
    data = get_json(r)

    log_found = False
    try:
        for log in data['data']:
            if re.search(creds['login'], log) and re.search(schema['name'], log):
                log_found = True
    except:
        cquit(Status.MUMBLE, f'Open log not working (JSON exception): {r.url}',f'Open log not working (JSON exception): {r.url}, content: {r.text}, expected login: {creds["login"]}, expected db name: {schema["name"]}')

    if not log_found:
        cquit(Status.MUMBLE, f'Open log not working: {r.url}',f'Open log not working: {r.url}, content: {r.text}, expected login: {creds["login"]}, expected db name: {schema["name"]}')

    # Getting info about user's databases

    r = requests.get(f'http://{host}:{PORT}/dbs', headers=auth_header)
    check_status_code(r)
    data = get_json(r)
    try:
        if data['data'][0]['db_name'] != schema['name']:
            cquit(Status.MUMBLE, f'Database name changed: {r.url}',f'Database name changed: {r.url}, content: {r.text}, expected name: {schema["name"]}, recived name: {data["data"][0]["db_name"]}')
        if data['data'][0]['description'] != schema['description']:
            cquit(Status.MUMBLE, f'Database description changed: {r.url}',f'Database description changed: {r.url}, content: {r.text}, expected description: {schema["description"]}, recived description: {data["data"][0]["description"]}')
    except:
        cquit(Status.MUMBLE, f'Can not get databases (JSON exception): {r.url}',f'Can not get databases (JSON exception): {r.url}, content: {r.text}')

    # API check
    # Getting chema

    r = requests.get(f'http://{host}:{PORT}/api/v1/dbs', params={'key': api_key})
    check_status_code(r)
    data = get_json(r)

    try:
        tables = []
        is_db_was_found = False
        for db_schema in data['data']:
            if db_schema['db_name'] == schema['name']:
                is_db_was_found = True
                tables = db_schema['tables']
    except:
        cquit(Status.MUMBLE, f'Database not found in db schema (JSON exception): {r.url}',f'Database not found in db schema (JSON exception): {r.url}, content: {r.text}')

    if not is_db_was_found:
        cquit(Status.MUMBLE, f'Database not found in db schema: {r.url}',f'Database not found in db schema: {r.url}, content: {r.text}')

    try:
        expected_tables = []
        for table in schema['tables']:
            expected_cols = []
            for col in table['columns']:
                expected_cols.append({'column_name': col['columnName'], 'value': col['varType']})
            expected_tables.append({'row': expected_cols, 'table_name': table['tableName']})
    except:
        cquit(Status.MUMBLE, f'Database schema error: {r.url}',f'Database schema error (error while parsing JSON (cheker maybe crash)): {r.url}, content: {r.text}')

    try:
        result = json_tools.diff(tables, expected_tables)
    except:
        cquit(Status.MUMBLE, f'Database schema error: {r.url}',f'Database schema error (error while compare JSON (json_tool.diff not working)): {r.url}, content: {r.text}')

    if result:
        cquit(Status.MUMBLE, f'Received and expected schema do not match: {r.url}',f'Received and expected schema do not match: {r.url}, content: {r.text}, excpected: {expected_tables}, recived: {tables}, diff: {result}')
    
    # Placing data
    
    data_to_place = {
        "row": [
        
        ]
    }

    t_count = len(schema['tables'])
    selected_table = random.randint(0, t_count - 1)
    

    for col in schema['tables'][selected_table]['columns']:
        if col['varType'] == 'TEXT' or col['varType'] == 'BLOB':    
            data_to_place['row'].append({'column_name': col['columnName'], 'value': get_random_word()})
        else:
            data_to_place['row'].append({'column_name': col['columnName'], 'value': str(random.randint(0, 999999))})

    r = requests.post(f'http://{host}:{PORT}/api/v1/', params={
            'key': api_key, 
            'db': schema['name'],
            'table': schema['tables'][selected_table]['tableName']
        }, json=data_to_place)
    check_status_code(r)
    data = get_json(r)

    # Getting data from db

    r = requests.get(f'http://{host}:{PORT}/api/v1/', params={
            'key': api_key, 
            'db': schema['name'],
            'table': schema['tables'][selected_table]['tableName']
        })
    check_status_code(r)
    data = get_json(r)

    try:
        for row in data_to_place['row']:
            if row['value'] in str(data['data'][0]):
                pass
            else:
                cquit(Status.MUMBLE, f'Can not get data from database {r.url}',f'Recived data from database doesn\'t mach with placed data: {r.url}, content: {r.text}, excpected: {data_to_place}, recived: {data}')
    except:
        cquit(Status.MUMBLE, f'Can not get data from database (JSON exception): {r.url}',f'Can not get data from database (JSON exception): {r.url}, content: {r.text}, excpected: {data_to_place}, recived: {data}')
    
    cquit(Status.OK, f'OK')

def put(host, flag_id, flag, vuln_number):
    if int(vuln_number) == 1:  # first vuln
        # Placing flag to database description

        r = requests.get(f'http://{host}:{PORT}/')
        check_status_code(r)

        creds = {"login":get_random_name(),"password":get_password()}

        # Register

        r = requests.post(f'http://{host}:{PORT}/register', json=creds)
        check_status_code(r)
        data = get_json(r)

        # Login
    
        r = requests.post(f'http://{host}:{PORT}/login', json=creds)
        check_status_code(r)
        data = get_json(r)

        try:
            token = data["data"]["jwt"]
        except:
            cquit(Status.MUMBLE, f'Can not get auth token: {r.url}',f'Can not get auth token: {r.url}, content: {r.text}')
        
        auth_header = {'Authorization': f'Bearer {token}'}

        schema = {
            "name":random.choice(db_names),
            "description": flag,
            "tables":[
                {
                    "tableName":random.choice(table_names) + str(random.randint(100, 999)),
                    "columns":[
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        },
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        }
                    ]
                },
                {
                    "tableName":random.choice(table_names) + str(random.randint(100, 999)),
                    "columns":[
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"INTEGER"
                        },
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        },
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        }
                    ]
                }
            ]
        }

        # Placing flag

        r = requests.post(f'http://{host}:{PORT}/new_db', headers=auth_header, json=schema)
        check_status_code(r)
        data = get_json(r)

        flag_id = str(creds).replace("\'", "\"")

        cquit(Status.OK, "OK", f'{flag_id}')

    elif int(vuln_number) in (2, 3, 4):  # second vuln
        # Placing flag in database data
        
        r = requests.get(f'http://{host}:{PORT}/')
        check_status_code(r)

        creds = {"login":get_random_name(),"password":get_password()}

        # Register

        r = requests.post(f'http://{host}:{PORT}/register', json=creds)
        check_status_code(r)
        data = get_json(r)

        # Login
    
        r = requests.post(f'http://{host}:{PORT}/login', json=creds)
        check_status_code(r)
        data = get_json(r)

        try:
            token = data["data"]["jwt"]
        except:
            cquit(Status.MUMBLE, f'Can not get auth token: {r.url}',f'Can not get auth token: {r.url}, content: {r.text}')
        
        auth_header = {'Authorization': f'Bearer {token}'}

        # Getting api key

        r = requests.get(f'http://{host}:{PORT}/api_key', headers=auth_header)
        check_status_code(r)
        data = get_json(r)

        try:
            api_key = data["data"]["apikey"]
        except:
            cquit(Status.MUMBLE, f'Can not get api key: {r.url}',f'Can not get api key: {r.url}, content: {r.text}')

        schema = {
            "name":random.choice(db_names),
            "description": random.choice(descriptions),
            "tables":[
                {
                    "tableName":random.choice(table_names) + str(random.randint(100, 999)),
                    "columns":[
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        },
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        }
                    ]
                },
                {
                    "tableName":random.choice(table_names) + str(random.randint(100, 999)),
                    "columns":[
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"INTEGER"
                        },
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        },
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        }
                    ]
                }
            ]
        }

        # Creating database

        r = requests.post(f'http://{host}:{PORT}/new_db', headers=auth_header, json=schema)
        check_status_code(r)
        data = get_json(r)

        # Placing flag 

        data_to_place = {
            "row": [
            
            ]
        }

        t_count = len(schema['tables'])
        selected_table = random.randint(0, t_count - 1)
        

        for col in schema['tables'][selected_table]['columns']:
            if col['varType'] == 'TEXT' or col['varType'] == 'BLOB':    
                data_to_place['row'].append({'column_name': col['columnName'], 'value': flag})
            else:
                data_to_place['row'].append({'column_name': col['columnName'], 'value': str(random.randint(0, 999999))})

        r = requests.post(f'http://{host}:{PORT}/api/v1/', params={
                'key': api_key, 
                'db': schema['name'],
                'table': schema['tables'][selected_table]['tableName']
            }, json=data_to_place)
        check_status_code(r)
        data = get_json(r)

        cquit(Status.OK, "OK", f'{api_key}')

def get(host, flag_id, flag, vuln_number):

    if int(vuln_number) == 1:  # first vuln

        # Getting flag from database description

        creds = json.loads(flag_id)

        # Login

        r = requests.post(f'http://{host}:{PORT}/login', json=creds)
        check_status_code(r)
        data = get_json(r)

        try:
            token = data["data"]["jwt"]
        except:
            cquit(Status.MUMBLE, f'Can not get auth token: {r.url}',f'Can not get auth token: {r.url}, content: {r.text}')
        
        auth_header = {'Authorization': f'Bearer {token}'}

        # Getting db description and flag

        r = requests.get(f'http://{host}:{PORT}/dbs', headers=auth_header)
        check_status_code(r)
        data = get_json(r)

        if flag not in str(data):
            cquit(Status.CORRUPT, f'Couldn\'t find flag in database info')

        cquit(Status.OK, f'OK')

    elif int(vuln_number) in (2, 3, 4):  # second vuln

        # Getting flag from database data

        api_key = flag_id

        # Getting chema

        r = requests.get(f'http://{host}:{PORT}/api/v1/dbs', params={'key': api_key})
        check_status_code(r)
        data = get_json(r)
        
        dbs_data = ""

        for db in data['data']:
            for table in db['tables']:
                r = requests.get(f'http://{host}:{PORT}/api/v1/', params={
                        'key': api_key, 
                        'db': db['db_name'],
                        'table': table['table_name']
                    })
                check_status_code(r)
                get_json(r)
                dbs_data += r.text

        if flag not in dbs_data:
            cquit(Status.CORRUPT, f'Couldn\'t find flag in database')

        cquit(Status.OK, f'OK')

if __name__ == '__main__':
    action, *args = sys.argv[1:]

    try:
        if action == 'check':
            host, = args
            check(host)

        elif action =='put':
            host, flag_id, flag, vuln_number = args
            put(host, flag_id, flag, vuln_number)

        elif action == 'get':
            host, flag_id, flag, vuln_number = args
            get(host, flag_id, flag, vuln_number)
        else:
            cquit(Status.ERROR, 'System error', 'Unknown action: ' + action)

        cquit(Status.ERROR)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        cquit(Status.DOWN, 'Connection error')
    except SystemError as e:
        raise
    except Exception as e:
        cquit(Status.ERROR, 'System error', str(e))