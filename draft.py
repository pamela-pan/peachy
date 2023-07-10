data = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Choose the tonality of my responses:",
				"emoji": True
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": ":art: Creative"
					},
					"value": "click_me_123",
					"action_id": "approve_button"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": ":raised_hands: Balanced"
					},
					"value": "click_me_123",
					"action_id": "deny_button"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": true,
						"text": ":bar_chart: Precise"
					},
					"value": "click_me_123",
					"action_id": "deny_button2"
				}
			]
		}
	]
}

RADIO_BUTTON_BLOCK = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Check out these rad radio buttons"
			},
			"accessory": {
				"type": "radio_buttons",
				"action_id": "temperature_control",
				"initial_option": {
					"value": "A1",
					"text": {
						"type": "plain_text",
						"text": "Radio 1"
					}
				},
				"options": [
					{
						"value": "A1",
						"text": {
							"type": "plain_text",
							"text": "Radio 1"
						}
					},
					{
						"value": "A2",
						"text": {
							"type": "plain_text",
							"text": "Radio 2"
						}
					}
				]
			}
		}
	]
}

# radio buttons
@app.action("temperature_control")
def handle_temp_control(ack,client,body,logger):
    ack()
    logger.info(body)
    print("temp control working")
    # print(body)
    button_state = body['state']
    print('state',button_state)
    block_id = body['message']['blocks'][0]['block_id']
    print('block id',block_id)
    button_value = button_state['values'][block_id]['temperature_control']['selected_option']['value']
    print("this is button value", button_value)
    
home_block ={
	"type": "home",
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "⚡️ *Hello, productivity superheroes!*",
				"emoji": True
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": " It's time to meet your sidekick, Jake (TBD), powered by the latest *Google PaLM 2* model. With its lightning-fast responses, clever suggestions, and witty banter, together we'll conquer deadlines, tackle challenges, and conquer the world (of work)!"
			},
			"accessory": {
				"type": "image",
				"image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQuQE5J5CteX9vz306v2GaMgy_wfqgv1BISzw&usqp=CAU",
				"alt_text": "calendar thumbnail"
			}
		},
		{
			"type": "divider"
		}
	]
}