<?php include('server.php') ?>
<?php include('header.php') ?>
<div class = "content" style="text-align:center; overflow:auto; height:500px">
	<?php if (isset($_SESSION['name'])):?>
	Hi, <?php echo '<strong>'.$_SESSION['name'].'</strong>'?>!
	<p></p>If you're interested in contributing to further development of M.E.R.C corporation, we would suggest buying our shares at $MERC.
	<a href='invest.php?merc_id=<?php echo merc_id($_SESSION['name']);?>'><p/><img src="image.php?advert"></a>
	<?php else:?>
	<img src="image.php?advert">
<?php endif;?>
</div>
<?php include('footer.php') ?>