from aiogram import types
from .logger_config import logger
from .steem_request import Blockchain

steem = Blockchain()

def search_steem_community(filter, offset):            
        inline_results = []
        try:
            results = steem.get_steem_community(filter) 
            MAX_RESULTS_PER_PAGE = 20
            paginated_results = results[offset:offset + MAX_RESULTS_PER_PAGE]

            for result in paginated_results:
                name = result['name']
                Title = result['title']
                id = result['id']
                desciption = result['about']

                inline_result = types.InlineQueryResultArticle(
                    id=f"{id}",
                    title=Title,                 
                    description=desciption,
                    input_message_content=types.InputTextMessageContent(
                        message_text=name
                    )
                )
                inline_results.append(inline_result)
                next_offset = str(offset + MAX_RESULTS_PER_PAGE) if len(results) > offset + MAX_RESULTS_PER_PAGE else None
            return inline_results, next_offset
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)

def view_steem_communit_post(community, offset):            
        inline_results = []
        try:
            results = steem.get_steem_community_post(community)
            MAX_RESULTS_PER_PAGE = 20
            paginated_results = results[offset:offset + MAX_RESULTS_PER_PAGE]

            for result in paginated_results:
                Title = result['title']
                id = result['post_id']
                #desciption = result['body']
                url = result['url']
                thumbnail_url=result['json_metadata']['image'][0]

                inline_result = types.InlineQueryResultArticle(
                    id=f"{id}",
                    title=Title,                 
                    thumbnail_url=thumbnail_url,
                    #description=desciption,
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"https://steemit.com{url}"
                    )
                )
                inline_results.append(inline_result)
                next_offset = str(offset + MAX_RESULTS_PER_PAGE) if len(results) > offset + MAX_RESULTS_PER_PAGE else None
            return inline_results, next_offset
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)