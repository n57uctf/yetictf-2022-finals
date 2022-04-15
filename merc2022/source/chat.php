<?php include('server.php')?>
<?php include('header.php')?>
<div class="content">
	<p style="color:purple; text-align: center; font-size:11px"><strong>✨<img src="media/chat.gif" height=30px>✨</strong></p>
	<form method="post" action="chat.php">
	<input hidden type="text" name="sender_id" value="<?php if(isset($_SESSION['merc_id'])) : echo $_SESSION['merc_id']; elseif (isset($_SESSION['driver_id'])) : echo $_SESSION['driver_id']; else : echo ""; endif;?>">
	<table style="width:700px">
		<tr>
			<td>
				<pre><div style="width: 470px;word-wrap: break-word; height: 400px;overflow:auto; display:flex; flex-direction:column-reverse; white-space:pre-wrap"><?php 
					if(isset($_SESSION['merc_id'])) : $receiver_id = $_SESSION['merc_id']; elseif (isset($_SESSION['driver_id'])) : $receiver_id = $_SESSION['driver_id']; else: $receiver_id = ''; endif;
					$results = pg_query(pg_connect($_SESSION['db_string']),"SELECT * FROM chat WHERE receiver_id = 'none' OR receiver_id='$receiver_id' OR sender_id='$receiver_id'");
					if (pg_num_rows($results) != 0) {
						$messages = pg_fetch_all($results);
						foreach ($messages as &$item) { if ($item['receiver_id']==$receiver_id) : echo '['.$item['timemark'].'] [DM] '.$item['name'].': '.$item['message'].'<br>'; elseif ($item['receiver_id']!= 'none') : echo '['.$item['timemark'].'] [DM] '.$item['name'].': '.$item['message'].'<br>'; else : echo '['.$item['timemark'].'] '.$item['name'].': '.$item['message'].'<br>'; endif; }
					} else { echo 'No messages!'; }
				?></div></pre>
			</td>
			<td>
				<pre><div style="height: 400px; width: 200px;overflow-x:hidden; overflow-y:auto;">    members list
-----------------------------------<?php 
				echo '<div class="field-row"><input checked type="radio" id="all" name="receiver_id" value="none"><label for="all">All</label></div>';
				$results = pg_query(pg_connect($_SESSION['db_string']),"SELECT * FROM merchants");
				if (pg_num_rows($results) != 0) {
					$members = pg_fetch_all($results);
					foreach ($members as &$item):
						echo '<div class="field-row"><input type="radio" id="'.$item['merc_id'].'" name="receiver_id" value="'.$item['merc_id'].'"><label for="'.$item['merc_id'].'">[MERC] '.$item['name'].'</label></div>';
					endforeach;
				}
				$results = pg_query(pg_connect($_SESSION['db_string']),"SELECT * FROM drivers");
				if (pg_num_rows($results) != 0) {
					$members = pg_fetch_all($results);
					foreach ($members as &$item):
						echo '<div class="field-row"><input type="radio" id="'.$item['driver_id'].'" name="receiver_id" value="'.$item['driver_id'].'"><label for="'.$item['driver_id'].'">[DRV] '.$item['name'].'</label></div>'; endforeach;
				}
				?></pre></div>
			</td>
		</tr>
		<tr>
			<td>
				<pre>X:&#92;M.E.R.C.OS&#92;v2><input type="text" name="message" style="width:300px; background-color:black; color:lightgrey;font-family:Perfect DOS VGA\ 437 Win; font-size:16px; border: black;"></pre>
			</td>
			<td>
				<pre><button type="submit" class="btn" name="chat">--send</button></pre>
			</td>
		</tr>
	</table>
</form>
</div>
<?php include('footer.php')?>