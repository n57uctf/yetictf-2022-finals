</div>
</div>
</div>
<div class="addition" style="grid-area: D">
	<div class="window">
    <div class="window-body" style="height:200px">
      <form method="get">
    	<pre style="height:200px">
<?php if (isset($_SESSION['merc_id'])) : ?>
X:&#92;M.E.R.C.OS&#92;v2>
commands-list

<button type="submit" formaction="cabinet.php" class="btn">cabinet --get</button>

<button type="submit" formaction="request.php" class="btn">request --make</button>

<button type="submit" formaction="chat.php" class="btn">cabinet --chat</button>
<?php elseif (isset($_SESSION['driver_id'])) :?>
X:&#92;M.E.R.C.OS&#92;v2>
commands-list

<button type="submit" formaction="chat.php" class="btn">cabinet --chat</button>
</pre>
</form>
<?php else :?>
X:&#92;M.E.R.C.OS&#92;v2>
commands-list

Access denied
</pre>
<? endif;?>
    </div>
  </div>
</div>
<div class="advert" style="grid-area: F;">
  <div class="window">
    <div class="title-bar">
      <div class="title-bar-text">
         Advert
      </div>
    </div>
    <div class="window-body" style="height:360px">
    <?php if (isset($_SESSION['name'])) : ?>
      <a href="advert.php?name=<?php echo $_SESSION['name']?>"><img src="media/advert.jpg" style="width: 100%; height: 350px"></a>
    <?php else :?>
      <a href="driver.php"><img src="media/driver.jpeg" style="width: 100%; height: 350px"></a>
    <?php endif;?>
    </div>
  </div>
</div>
<div class="footer" style="grid-area: E">
  <div class="window">
    <div class="window-body">
      <pre>
      Made by MERC corp. in a cold month of February, 2003. 
                    All rights are wrong.</pre>
    </div>
  </div>
</div>
</div>
</div>
</body>
</html>