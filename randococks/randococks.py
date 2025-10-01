from redbot.core import commands
from redbot.core.bot import Red
import random
import datetime
from redbot.core import Config
import discord

class randococks(commands.Cog):
  def __init__(self, bot: Red):
    self.bot = bot
    self.config = Config.get_conf(self, identifier=1027)
    self.config.register_global(
        conf_current_week = 0,
        conf_current_seed = 1304
    )

    self.middle_list = ["All-Beef Thermometer", "21st Digit", "Ace In The Hole", "Acorn Andy", "Action Jackson", "Adam Halfpint", "Admiral Winky", "African Black Snake", "Afro Man", "AIDS Baster", "AIDS Grenade", "Alabama Blacksnake", "Albino Cave Dweller", "All-Day Sucker", "Anaconda", "Anal Impaler", "Anal Intruder", "Anal Spear", "Ankle Spanker", "Apple-Headed Monster", "Ass Blaster", "Ass Pirate", "Ass Wedge", "Astralgod", "Auger-Headed Gut Wrench", "Baby Maker", "Baby's Arm Holding An Apple", "Baby's Arm In A Boxing Glove", "Bacon Bazooker", "Bacon Rod", "Badboy", "Bagpipe", "Bald Avenger", "Bald Butler", "Bald-Headed Beauty", "Bald-Headed Giggle Stick", "Bald-Headed Hermit", "Bald-Headed Jesus", "Bald-Headed Yogurt Slinger", "Bald-Headed Spunk-Juice Dispenser", "Ball Buddy", "Baloney Pony", "Banana", "Bat And Balls", "Battering Ram", "Bayonet", "Bavarian Beefstick", "Beard Splitter", "Bearded Blood Sausage", "Bearded Burglar", "Beastus Maximus", "Beaver Buster", "Beaver Cleaver", "Bed Snake", "Beef Baton", "Beef Bayonet", "Beef Belt Buckle", "Beef Bugle", "Beef Bus", "Beef Missile", "Beef Soldier", "Beef Stick", "Beefy McManstick", "Bell Rope", "Belly Stick", "Best Leg Of Three", "(Big) Beanpole", "Big & The Twins", "Big Us", "Big Jake The One-Eyed Snake", "Big Jim And The Twins", "Big Johnson", "Big Lebowski", "Big Number One", "Big Mac", "Big Red", "Big Rod", "Big Uncle", "Biggus Us", "Bilbo Baggins", "Bishop", "Bishop With His Nice Red Hat", "Blaster", "Stick", "Bits And Pieces", "Blind Butler", "Blind Snake", "Blinky", "Blood Blunt", "Blood Slug", "Blood Sword", "Blow Pop", "Blowtorch", "Blue Steel", "Blue-Veined Jackhammer", "Blue-Veined Junket Pumper", "Blue-Veined Piccolo", "Blue-Veined Puss Chucker", "Blue-Veiner", "Blunt", "Bob", "Bob Dole", "Bob Johnson", "Bobo", "Bone", "Bone Phone", "Bone Rollercoaster", "Boneless Beef", "Boneless Fish", "Boner", "Boney Cannelloni", "Bone-Her", "Bookmark", "Bop Gun", "Bottle Rocket", "Bow-Legged Swamp Donkey", "Box Buster", "Boybrush", "Bradford And The Pair", "Bratwurst", "Breakfast Burrito", "Breakfast Wood", "Broom", "Brutus", "Bubba", "Bulbulous Big-Knob", "Bumtickler", "Bush Beater", "Bush Rusher", "Bushwhacker", "Hymen Buster", "Buster McThunderstick", "Butt Blaster", "Butt Pirate", "Butter Churn", "Butterknife", "Candy Cane", "Canelo", "Caped Crusader", "Captain Bilbo", "Captain Crook", "Captain Hook", "Captain Howdy", "Captain Kirk", "Captain Winky", "Carnal Stump", "Cattle Prod", "Cave Hunter", "Cax", "Cervix Crusader", "Cervix Pounder", "Chancellor", "Chap", "Charlie Russell The One-Eyed Muscle", "Cheese Staff", "Cherry Picker", "Cherry Poppin' Daddy", "Cherry Splitter", "Chi Zi Wang", "Chick Sticker", "Chicksicle", "Chief Of Staff", "Chimbo", "Chimney Cleaner", "Choo-Choo", "Choad (Chode)", "Chorizo", "Chowder Dumper", "Chubby", "Chubby Conquistador", "Chum", "Chunk 'o' Love", "Chunder Thunder", "Cigar", "Circus Boy", "Clam Digger", "Clam Hammer", "Clam Sticker", "Clit Tickler", "Cob", "Codger", "Colon Cowboy", "Colon Crusader", "Colossus", "Coral Branch", "Corndog", "Cornholer", "Cornstalk", "Cornstalk Cowboy", "Crack Hunter", "Crack Smacker", "Cramstick", "Crank", "Crank Shaft", "Cream-Filled Meat Stick", "Cream Bandit", "Cream Cannon", "Creamsicle", "Creamstick", "Cream Spritzer", "Crimson Chitterling", "Crimson Darth Vader", "Crippler", "Crotch Cobra", "Crotch Cowboy", "Crotch Rocket", "Crotch Vomiter", "Crushin' Russian", "Cum Pump", "Cummingtonite", "Cunny-Catcher", "Cunt Destroyer", "Cupid's Arrow", "Curious George", "Custard Cannon", "Custard Pump", "Cyclops", "Daddy Long-Stroke", "Danger The One-E Ranger", "Danglin' Fury", "Danglin' Wang", "Dangling Participle", "Dart Of Love", "Darth Vader", "Davy Crockett", "Deep-Veined Purple-Helmeted Spartan Of Love", "Demeanor", "Diamond Cutter", "Digit", "Diller", "Dilly-Ho-Ho", "Ding-A-Ling", "Ding-Dong", "Dingaroo", "Dingle", "Dingle Dangle", "Dingledong", "Dinglehopper", "Dingus", "Dingy", "Dinky", "Dipstick", "Dirk Diggler", "Divining Rod", "Dobber", "Docking Tube", "Dog Knot", "Dolphin", "Dong", "Dong-Bong", "Dong-Stick", "Dongle", "Donker", "Donkey Kong", "Doo-Dad", "Doo-Dar", "Doodle"]
    self.ending_list = ["Now that's a waifu destroyer!", 'Time to stuff some chocolate!', "NOW THAT'S A GACHI STEAK!", 'Woa!', 'Amazing!', 'Sugooiiii', 'OwO!', '[glomps]', 'UwU', 'I wish I had one that big!', 'Kawaii!!!', 'GOOOOLDEN cock!', 'COCKADOODLEDOOOO!!!', 'WAAAAOW', 'Insane!']

  @commands.command()
  async def cock(self, ctx, *args):
    # get seed and month
    saved_month = await self.config.conf_current_month()
    saved_week = await self.config.conf_current_week()
    saved_seed = await self.config.conf_current_seed()

    # Weekly - check for re-roll
    now = datetime.datetime.now()
    new_week = now.isocalendar()[1]  # 1–53

    if new_week != saved_week:
        new_seed = random.randint(1, 10000)
        await self.config.conf_current_week.set(new_week)
        await self.config.conf_current_seed.set(new_seed)

        saved_seed = new_seed
        await ctx.send(
            'NEW COCK! GET YER NEW COCK OF THE WEEK HERE!'
        )

    # handle checking someone elses cock
    author_id  = int(ctx.author.id)
    if len(args) != 0:
      target = args[0]
      if target[:3] == '<@!':
        author_id = int(target[3:-1])
      else:
        member = ctx.guild.get_member_named(target)
        if member is None:
          await ctx.send(str(ctx.author.name) + " that isn't a real person. stop being retarded.")
          return
        author_id = member.id

    #user = discord.utils.get(ctx.guild.members, id=str(author_id))
    user = await self.bot.fetch_user(str(author_id))
    random.seed(saved_seed * author_id)
    length = (random.randint(1, 125) * 0.1)
    length_string = "{:.1f}".format(length)
    if length_string[-1] == '0':
      length_string = length_string[:-2]
    random.seed()
    await ctx.send('Looks like ' + user.display_name + "'s " + self.middle_list[random.randint(0, len(self.middle_list) - 1)] + ' is ' + length_string + ' inches long! ' + self.ending_list[random.randint(0, len(self.ending_list) - 1)])
