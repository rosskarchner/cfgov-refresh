import mock
from django.test import RequestFactory, TestCase

from v1.handlers.blocks.feedback import FeedbackHandler


class TestFeedbackHandler(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        page = mock.Mock()
        post_data = {
            'is_helpful': '1',
            'comment': 'Example comment.'
        }
        request = self.factory.post('/', post_data)
        self.handler = FeedbackHandler(page, request, None)

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.get_response')
    @mock.patch('v1.handlers.blocks.feedback.FeedbackForm')
    def test_process_binds_form_for_submissions(self, mock_form, mock_get_response):
        self.handler.process(is_submitted=True)
        mock_form.assert_called_with(self.handler.request.POST)

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.get_response')
    @mock.patch('v1.handlers.blocks.feedback.FeedbackForm')
    def test_process_calls_get_response_for_submissions(self, mock_form, mock_get_response):
        self.handler.process(is_submitted=True)
        mock_get_response.assert_called_with(mock_form())

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.get_response')
    @mock.patch('v1.handlers.blocks.feedback.FeedbackForm')
    def test_process_does_not_bind_form_non_submissions(self, mock_form, mock_get_response):
        self.handler.process(is_submitted=False)
        mock_form.assert_called_with()

    @mock.patch('v1.handlers.blocks.feedback.FeedbackForm')
    def test_process_returns_context(self, mock_form):
        result = self.handler.process(False)
        self.assertEqual(result, {'form': mock_form()})

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.get_response')
    def test_process_returns_get_response_call_for_submission(self, mock_get_response):
        result = self.handler.process(True)
        self.assertEqual(result, mock_get_response())

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.fail')
    def test_get_response_calls_form_isvalid(self, mock_fail):
        form = mock.Mock()
        form.is_valid.return_value = False
        self.handler.get_response(form)
        self.assertTrue(form.is_valid.called)

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.fail')
    def test_get_response_calls_calls_fail_for_invalid_form(self, mock_fail):
        form = mock.Mock()
        form.is_valid.return_value = False
        self.handler.get_response(form)
        mock_fail.assert_called_with(form)

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.success')
    def test_get_response_sets_attrs(self, mock_success):
        form = mock.Mock()
        self.handler.get_response(form)
        self.assertTrue(form.save().is_helpful)
        self.assertEqual(form.save().page, self.handler.page)

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.success')
    def test_get_response_saves_feedback(self, mock_success):
        form = mock.Mock()
        self.handler.get_response(form)
        self.assertTrue(form.save.called)

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.success')
    def test_get_response_calls_sucess_for_valid(self, mock_success):
        form = mock.Mock()
        self.handler.get_response(form)
        self.assertTrue(mock_success.called)

    @mock.patch('v1.handlers.blocks.feedback.HttpResponseRedirect')
    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_success_calls_JsonResponse_for_ajax(self, mock_messages, mock_json_response, mock_redirect):
        self.handler.request = self.factory.post('/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.handler.success()
        mock_json_response.assert_called_with({'result': 'pass'})

    @mock.patch('v1.handlers.blocks.feedback.HttpResponseRedirect')
    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_sucess_returns_JsonResponse_for_ajax(self, mock_messages, mock_json_response, mock_redirect):
        self.handler.request = self.factory.post('/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        result = self.handler.success()
        self.assertEqual(result, mock_json_response())

    @mock.patch('v1.handlers.blocks.feedback.HttpResponseRedirect')
    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_sucess_calls_messages_for_nonajax(self, mock_messages, mock_json_response, mock_redirect):
        self.handler.success()
        self.assertTrue(mock_messages.success.called)

    @mock.patch('v1.handlers.blocks.feedback.HttpResponseRedirect')
    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_sucess_returns_redirect_for_nonajax(self, mock_messages, mock_json_response, mock_redirect):
        self.handler.success()
        mock_redirect.assert_called_with(self.handler.page.url)

    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_fail_calls_returns_JsonResponse_with_ajax_request(self, mock_messages, mock_json_response):
        form = mock.Mock()
        self.handler.request = self.factory.get('/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        result = self.handler.fail(form)
        mock_json_response.assert_called_with({'result': 'fail'})

    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_fail_calls_message_error_with_helpful_message_for_helpful_error(self, mock_messages, mock_json_response):
        form = mock.Mock()
        form.errors.get.return_value = True
        self.handler.fail(form)
        mock_messages.error.assert_called_with(self.handler.request, 'You must select an option.')

    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_fail_calls_message_error_with_other_message(self, mock_messages, mock_json_response):
        form = mock.Mock()
        form.errors.get.return_value = False
        self.handler.fail(form)
        mock_messages.error.assert_called_with(self.handler.request, 'Something went wrong. Please try again.')

    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_fail_calls_returns_form_dict(self, mock_messages, mock_json_response):
        form = mock.Mock()
        result = self.handler.fail(form)
        self.assertEqual(result, {'form': form})
