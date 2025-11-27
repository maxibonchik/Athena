import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [testCompleted, setTestCompleted] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  // Загрузка вопросов при старте
  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      console.log('Загружаем вопросы...');
      const response = await fetch('http://localhost:8000/courses/api/cognitive-test/questions/');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Вопросы загружены:', data);
      setQuestions(data.questions);
      setLoading(false);
    } catch (error) {
      console.error('Error loading questions:', error);
      setError('Не удалось загрузить вопросы теста: ' + error.message);
      setLoading(false);
    }
  };

  const handleAnswer = (answer) => {
    const question = questions[currentQuestion];
    const newAnswers = {
      ...answers,
      [question.question_number]: answer
    };
    
    console.log('Ответ:', answer, 'Вопрос:', question.question_number);
    setAnswers(newAnswers);

    // Переход к следующему вопросу или завершение
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      submitTest(newAnswers);
    }
  };

  const submitTest = async (finalAnswers) => {
    try {
      console.log('Отправляем ответы:', finalAnswers);
      const response = await fetch('http://localhost:8000/courses/api/cognitive-test/submit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answers: finalAnswers }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Результаты теста:', data);
      setResults(data.results);
      setTestCompleted(true);
    } catch (error) {
      console.error('Error submitting test:', error);
      setError('Ошибка при отправке результатов: ' + error.message);
    }
  };

  const restartTest = () => {
    setCurrentQuestion(0);
    setAnswers({});
    setTestCompleted(false);
    setResults(null);
    setError(null);
    setLoading(true);
    loadQuestions();
  };

  // Функция для получения русского названия стиля обучения
  const getLearningStyleName = (style) => {
    const styles = {
      'visual': 'Визуал',
      'auditory': 'Аудиал', 
      'reading': 'Чтение/Письмо',
      'kinesthetic': 'Кинестет',
      'mixed': 'Смешанный'
    };
    return styles[style] || style;
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <h2>Загружаем вопросы теста...</h2>
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <div className="error-state">
          <h2>😕 Произошла ошибка</h2>
          <p>{error}</p>
          <div className="debug-info">
            <p><strong>Проверьте:</strong></p>
            <ul>
              <li>Запущен ли Django сервер на localhost:8000</li>
              <li>Настроены ли CORS заголовки в Django</li>
              <li>Доступен ли API по адресу: http://localhost:8000/courses/api/cognitive-test/questions/</li>
            </ul>
          </div>
          <button className="retry-btn" onClick={restartTest}>
            Попробовать снова
          </button>
        </div>
      </div>
    );
  }

  if (testCompleted && results) {
    return (
      <div className="app">
        <div className="results">
          <h1>🎉 Тест завершен!</h1>
          <div className="results-card">
            <h2>Ваш профиль обучения</h2>
            
            <div className="result-item">
              <span className="label">Стиль обучения:</span>
              <span className="value">{getLearningStyleName(results.learning_style)}</span>
            </div>
            
            <div className="result-item">
              <span className="label">Оценка памяти:</span>
              <span className="value">{results.memory_score}/10</span>
            </div>
            
            <div className="result-item">
              <span className="label">Самодисциплина:</span>
              <span className="value">{results.discipline_score}/10</span>
            </div>

            <div className="recommendations">
              <h3>💡 Рекомендации:</h3>
              <p>
                {results.learning_style === 'visual' && 'Вам подойдут видеоуроки, инфографика и схемы'}
                {results.learning_style === 'auditory' && 'Вам будут полезны подкасты и аудиолекции'}
                {results.learning_style === 'reading' && 'Лучше всего вы учитесь через чтение и конспекты'}
                {results.learning_style === 'kinesthetic' && 'Эффективнее всего практические задания и проекты'}
                {results.learning_style === 'mixed' && 'Вам подойдет комбинированный подход к обучению'}
              </p>
            </div>
          </div>
          
          <button className="continue-btn" onClick={restartTest}>
            Пройти тест еще раз
          </button>
        </div>
      </div>
    );
  }

  const question = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="app">
      <header className="app-header">
        <h1>🧠 Афина</h1>
        <p>Ваш персональный учитель</p>
      </header>
      
      <div className="test-container">
        <div className="progress-section">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="progress-text">
            Вопрос {currentQuestion + 1} из {questions.length}
          </div>
        </div>
        
        <div className="question-card">
          <h2 className="question-text">{question.question_text}</h2>
          
          <div className="options">
            <button 
              className="option-btn" 
              onClick={() => handleAnswer('a')}
            >
              <span className="option-letter">A</span>
              <span className="option-text">{question.options.a}</span>
            </button>
            
            <button 
              className="option-btn" 
              onClick={() => handleAnswer('b')}
            >
              <span className="option-letter">B</span>
              <span className="option-text">{question.options.b}</span>
            </button>
            
            <button 
              className="option-btn" 
              onClick={() => handleAnswer('c')}
            >
              <span className="option-letter">C</span>
              <span className="option-text">{question.options.c}</span>
            </button>
            
            <button 
              className="option-btn" 
              onClick={() => handleAnswer('d')}
            >
              <span className="option-letter">D</span>
              <span className="option-text">{question.options.d}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
const submitTest = async (finalAnswers) => {
  try {
    console.log('📤 Отправляем ответы на сервер:', finalAnswers);
    
    const response = await fetch('http://localhost:8000/courses/api/cognitive-test/submit/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ answers: finalAnswers }),
    });

    console.log('📥 Получен ответ, статус:', response.status);
    
    // Получаем текст ответа для отладки
    const responseText = await response.text();
    console.log('📄 Текст ответа:', responseText);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}, response: ${responseText}`);
    }

    // Парсим JSON
    const data = JSON.parse(responseText);
    console.log('✅ Данные ответа:', data);
    
    if (data.success) {
      setResults(data.results);
      setTestCompleted(true);
    } else {
      throw new Error(data.error || 'Неизвестная ошибка сервера');
    }
    
  } catch (error) {
    console.error('❌ Полная ошибка:', error);
    setError('Ошибка при отправке результатов: ' + error.message);
  }
};