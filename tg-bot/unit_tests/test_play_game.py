from unittest.mock import AsyncMock, call, patch

import pytest

import scenarios.play_game
from scenarios.play_game import start_game, change_to_larger, change_to_lower, end_game, States, get_keyboard
from unit_tests.mock_helpers import get_fsm_context_and_message_mock


@pytest.mark.asyncio
async def test_start_game_clears_state_data():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await start_game(message, fsm_context)

    data = await fsm_context.get_data()
    assert list(data.keys()) == ['rng']


@pytest.mark.asyncio
async def test_start_game_sets_correct_state_and_state_data():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await start_game(message, fsm_context)

    assert States.game_state == await fsm_context.get_state()
    data = await fsm_context.get_data()
    assert get_initial_game_range() == data['rng']


@pytest.mark.asyncio
async def test_start_game_reply_with_correct_answers():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await start_game(message, fsm_context)

    l, r, guess = get_initial_game_range()
    message.answer.assert_has_awaits(
        [call(f'Загадайте число от {l} до {r}. И через несколько секунд я попробую его отгадать'),
         call(f'Это число {guess}?', reply_markup=get_keyboard())],
        any_order=True
    )


@pytest.mark.asyncio
async def test_change_to_lower_modify_range_correctly():
    fsm_context, _ = await get_fsm_context_and_message_mock(dirty_state=False)
    await fsm_context.set_state(States.game_state)
    l, r, guess = get_initial_game_range()
    await fsm_context.update_data(rng=(l, r, guess))
    callback = AsyncMock()

    await change_to_lower(callback, fsm_context)

    data = await fsm_context.get_data()
    l2, r2, new_guess = data['rng']
    assert r2 == guess - 1
    assert l2 == l
    assert new_guess == (l2 + r2) // 2
    callback.message.edit_text.assert_has_awaits(
        [call(f'Это число {new_guess}?', reply_markup=get_keyboard())])


@pytest.mark.asyncio
async def test_change_to_larger_modify_range_correctly():
    fsm_context, _ = await get_fsm_context_and_message_mock(dirty_state=False)
    await fsm_context.set_state(States.game_state)
    l, r, guess = get_initial_game_range()
    await fsm_context.update_data(rng=(l, r, guess))
    callback = AsyncMock()

    await change_to_larger(callback, fsm_context)

    data = await fsm_context.get_data()
    l2, r2, new_guess = data['rng']
    assert l2 == guess + 1
    assert r2 == r
    assert new_guess == (l2 + r2) // 2
    callback.message.edit_text.assert_has_awaits(
        [call(f'Это число {new_guess}?', reply_markup=get_keyboard())])


@pytest.mark.asyncio
async def test_end_game_makes_bot_to_send_start_message():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)
    callback = AsyncMock()
    callback.message = message

    with patch.object(scenarios.play_game, "show_start_message", new=AsyncMock()):
        await end_game(callback, fsm_context)
        scenarios.play_game.show_start_message.assert_awaited_once_with(callback.message, fsm_context)


def test_get_keyboard():
    (lower_btn, larger_btn), (equal_btn,) = get_keyboard().inline_keyboard
    assert lower_btn.text == 'Меньше'
    assert lower_btn.callback_data == 'lower'
    assert larger_btn.text == 'Больше'
    assert larger_btn.callback_data == 'larger'
    assert equal_btn.text == 'В самый раз'
    assert equal_btn.callback_data == 'equal'


def get_initial_game_range():
    return 1, 100, (1 + 100) // 2
