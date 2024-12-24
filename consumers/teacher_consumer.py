from sqlalchemy.exc import SQLAlchemyError

from consumers.consumer_service import decode_kafka_message, create_consumer
from database import db_session
from models.teacher import Teacher



def process_teacher_messages(sql_consumer):
    try:
        for message in sql_consumer:
            row = decode_kafka_message(message)
            if not row.get('name'):
                print(f"the following line is not a teacher {row}")
                continue
            teacher = Teacher(**row)
            teacher_exists = db_session.query(Teacher).filter(Teacher.id == teacher.id).first()
            if teacher_exists:
                print(f"teacher {teacher.id} already exists")
                continue
            db_session.add(teacher)
            db_session.commit()
            sql_consumer.commit()
        return None
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error processing message: {e}")

def main():
    teacher_consumer = create_consumer('teachers')
    process_teacher_messages(teacher_consumer)

if __name__ == '__main__':
    main()