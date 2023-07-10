TONE_BUTTON_BLOCK = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "You've started a new conversation!! \n Choose the tonality of my responses:",
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
					"action_id": "creative_tone"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": ":raised_hands: Balanced"
					},
					"value": "click_me_123",
					"action_id": "balanced_tone"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": ":bar_chart: Precise"
					},
					"value": "click_me_123",
					"action_id": "precise_tone"
				}
			]
		}
	]
}