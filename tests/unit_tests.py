from base import *


class AuthTest(GeneralTest):

    def test_can_pick_up_api_key_with_relative_path(self):
        key = public_api.get_api_key('./files/dummy_api_key')
        self.assertEqual('FFFFFFFFI8005cfn4Mhhhhhhhh2WI5m11114090', key)

class QueryTest(GeneralTest):

    def test_api_call_gets_a_response(self):
        response = public_api.make_api_call(self.leekspin_id)
        self.assertNotEqual(response, '')

    def test_id_in_response(self):
        leekspin = public_api.get_videos([self.leekspin_id])[0]
        self.assertEqual(self.leekspin_id, leekspin['id'])

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


class InputTest(GeneralTest):

    def test_can_get_help_when_running_script_from_cmd(self):
        output = sp.check_output([self.script, '-h'])
        self.assertIn("show this help message and exit", output)

class OutputTest(GeneralTest):

    def test_a_csv_file_can_be_output(self):
        leekspin = public_api.get_videos([self.leekspin_id])
        public_api.output_to_csv(leekspin, self.output)
        self.assertTrue(os.path.exists(self.output))

    def test_unicode_not_a_problem(self):
        dummy_vid = {'name': u'\u2019'}
        public_api.output_to_csv([dummy_vid], self.output)


if __name__ == '__main__':
     unittest.main()
