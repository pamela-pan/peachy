class HomeDisplay:
    APP_DESCRIPTION = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":zap: *Hello, productivity superheroes!*"
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
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":speech_balloon: *Try the following prompts:*"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "* Generate code comments for my Korean colleague \n * Design a collaborative filtering algorithm for personalized movie recommendations. \n * Draft a Holiday marketing plan for an ecommerce platform"
			}
		}
	]

    def __init__(self, client, event, logger):
        self.client = client
        self.event = event
        self.logger = logger

    def display_home(self):
        try:
            self.client.views_publish(
                user_id=self.event["user"],
                view={
                "type": "home",
                "callback_id": "home_view",
                "blocks": 
                    self.APP_DESCRIPTION  # Reference the APP_DESCRIPTION variable here
                
            }
            )
        except Exception as e:
            self.logger.error(f"Error in display_home: {str(e)}")