from base import *

class QueryTest(GeneralTest):

    def test_id_in_response(self):
        leekspin = public_api.get_videos([self.leekspin_id])[0]
        self.assertEqual(self.leekspin_id, leekspin['id'])

    def test_link_in_response(self):
        leekspin = public_api.get_videos([self.leekspin_id])[0]
        self.assertEqual("youtu.be/" + self.leekspin_id, leekspin['link'])

    def test_can_get_video_name_from_id(self):
        leekspin = public_api.get_videos([self.leekspin_id])[0]
        self.assertEqual(u'Leek Spin', leekspin['name'])

    def test_can_get_channel_name_from_id(self):
        leekspin = public_api.get_videos([self.leekspin_id])[0]
        self.assertEqual(u'Xyliex', leekspin['channel_title'])

    def test_can_get_channel_description_from_id(self):
        leekspin = public_api.get_videos([self.leekspin_id])[0]
        description = u"Inoue from Bleach spinning a leek with my best" \
                      " attempt at editing the original song: Loituma - " \
                      "Ievan polkka (Ieva's Polka)."
        self.assertEqual(description, leekspin['description'])

    def test_can_get_video_published_time_and_date_in_multiple_formats(self):
        leekspin = public_api.get_videos([self.leekspin_id])[0]
        self.assertEqual('2006-09-26T02:45:35.000Z',
                         leekspin['published_datetime_iso'])
        self.assertEqual('26/09/2006', leekspin['published_date'])
        self.assertEqual('02:45:35', leekspin['published_time'])

    def test_can_get_view_comment_favourite_statistics(self):
        leekspin = public_api.get_videos([self.leekspin_id])[0]
        self.assertLessEqual(18150, leekspin['comment_count'])
        self.assertLessEqual(6475867, leekspin['view_count'])
        self.assertLessEqual(0, leekspin['favourite_count'])
        self.assertLessEqual(1120, leekspin['dislike_count'])
        self.assertLessEqual(31661, leekspin['like_count'])
        self.assertEqual(leekspin['like_count'] - leekspin['dislike_count'],
                         leekspin['approval'])

    def test_can_pass_multiple_ids_to_function(self):
        green_title = u'Change The Tune - Green Party 2015 Election Broadcast'
        videos = public_api.get_videos([self.leekspin_id, self.green_id])
        self.assertEqual(len(videos), 2)
        self.assertEqual([v['name'] for v in videos], [u'Leek Spin', green_title])

class CommentsTest(GeneralTest):

    def test_can_get_n_comments(self):
        returned = public_api.get_most_recent_comments(self.green_id, 69)
        self.assertEqual(len(returned['items']), 69)

    def test_asking_for_more_than_100_comments_fails(self):
        with self.assertRaises(ValueError):
            public_api.get_most_recent_comments(self.green_id, 400)

    def test_sorting_by_likes_works(self):
        response = public_api.get_most_recent_comments(self.leekspin_id, 20)
        sorted_comments = public_api.sort_comments_by_likes(response)
        like_count_to_lose_to = public_api.like_count(sorted_comments[0])
        for c in sorted_comments:
            message = "{} not less than {}".format(public_api.like_count(c),
                                                   like_count_to_lose_to)
            self.assertTrue(public_api.like_count(c) <= like_count_to_lose_to,
                            msg=message)
            like_count_to_lose_to = public_api.like_count(c)

    def test_sorting_by_replies_works(self):
        response = public_api.get_most_recent_comments(self.leekspin_id, 20)
        sorted_comments = public_api.sort_comments_by_replies(response)
        reply_count_to_lose_to = public_api.reply_count(sorted_comments[0])
        for c in sorted_comments:
            message = "{} not less than {}".format(public_api.reply_count(c),
                                                   reply_count_to_lose_to)
            self.assertTrue(public_api.reply_count(c) <= reply_count_to_lose_to,
                            msg=message)
            reply_count_to_lose_to = public_api.reply_count(c)

    def test_none_of_this_breaks_if_a_video_has_no_attention(self):
        # Not meant to error
        comments = public_api.get_most_recent_comments(self.big_dog_id, 20)
        self.assertEqual(comments['items'], [])
        video = public_api.get_videos([self.big_dog_id])
        public_api.output_to_csv(video, self.output)

if __name__ == '__main__':
     unittest.main()